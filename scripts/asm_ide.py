#!/usr/bin/env python3
"""Lightweight Tkinter editor/build runner for FloppyBootSuite."""
from pathlib import Path
import argparse
import shutil
import subprocess
import sys
import tkinter as tk
from tkinter import filedialog, messagebox, ttk

ROOT = Path(__file__).resolve().parents[1]
FOLDERS = ("asm", "boot", "stage2", "firmware", "os", "examples", "tests", "tools", "scripts", "language", "docs", "config")

def command(args):
    try:
        p = subprocess.run(args, cwd=ROOT, text=True, stdout=subprocess.PIPE,
                           stderr=subprocess.STDOUT, timeout=180)
        return p.returncode, p.stdout
    except (OSError, subprocess.TimeoutExpired) as exc:
        return 1, str(exc)

class IDE(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("FloppyBootSuite Assembly IDE")
        self.geometry("1100x720")
        self.current = None
        self.make_widgets()
        self.refresh_tree()
        self.write_log("Ready — F5 build, F6 lint, F9 QEMU.")

    def make_widgets(self):
        bar = ttk.Frame(self); bar.pack(fill="x")
        for title, fn in (("Open", self.open_dialog), ("Save", self.save),
                          ("Build F5", self.build), ("Lint F6", self.lint),
                          ("Run QEMU F9", self.run_qemu)):
            ttk.Button(bar, text=title, command=fn).pack(side="left", padx=3, pady=4)
        panes = ttk.Panedwindow(self, orient="horizontal"); panes.pack(fill="both", expand=True)
        left = ttk.Frame(panes, width=260); right = ttk.Frame(panes)
        panes.add(left, weight=1); panes.add(right, weight=4)
        self.tree = ttk.Treeview(left, show="tree"); self.tree.pack(fill="both", expand=True)
        self.tree.bind("<<TreeviewSelect>>", self.selected_file)
        self.editor = tk.Text(right, undo=True, wrap="none", font=("Consolas", 11))
        sy = ttk.Scrollbar(right, orient="vertical", command=self.editor.yview)
        sx = ttk.Scrollbar(right, orient="horizontal", command=self.editor.xview)
        self.editor.configure(yscrollcommand=sy.set, xscrollcommand=sx.set)
        self.editor.grid(row=0, column=0, sticky="nsew"); sy.grid(row=0, column=1, sticky="ns")
        sx.grid(row=1, column=0, sticky="ew")
        right.rowconfigure(0, weight=1); right.columnconfigure(0, weight=1)
        self.output = tk.Text(self, height=9, state="disabled", wrap="word", font=("Consolas", 10))
        self.output.pack(fill="x")
        self.bind("<Control-o>", lambda _e: self.open_dialog())
        self.bind("<Control-s>", lambda _e: self.save())
        self.bind("<F5>", lambda _e: self.build())
        self.bind("<F6>", lambda _e: self.lint())
        self.bind("<F9>", lambda _e: self.run_qemu())

    def write_log(self, message):
        self.output.configure(state="normal")
        self.output.insert("end", message.rstrip() + "\n")
        self.output.see("end")
        self.output.configure(state="disabled")

    def refresh_tree(self):
        self.tree.delete(*self.tree.get_children())
        for folder in FOLDERS:
            base = ROOT / folder
            if not base.is_dir(): continue
            parent = self.tree.insert("", "end", text=folder, open=True, values=(str(base),))
            for path in sorted(base.rglob("*")):
                if path.is_file() and not any(part in {".git", "build", "__pycache__"} for part in path.parts):
                    self.tree.insert(parent, "end", text=str(path.relative_to(base)), values=(str(path),))

    def selected_file(self, _event=None):
        selection = self.tree.selection()
        if not selection: return
        values = self.tree.item(selection[0], "values")
        if values and Path(values[0]).is_file(): self.open_file(Path(values[0]))

    def open_file(self, path):
        path = path.resolve()
        if ROOT not in path.parents:
            messagebox.showerror("Blocked", "Open files inside this repository only."); return
        try:
            self.current = path
            self.editor.delete("1.0", "end")
            self.editor.insert("1.0", path.read_text(encoding="utf-8"))
            self.title("FloppyBootSuite Assembly IDE — " + str(path.relative_to(ROOT)))
        except OSError as exc: messagebox.showerror("Open failed", str(exc))

    def open_dialog(self):
        name = filedialog.askopenfilename(initialdir=ROOT, filetypes=[("Project files", "*.asm *.inc *.py *.json *.md *.txt"), ("All files", "*.*")])
        if name: self.open_file(Path(name))

    def save(self):
        if self.current is None:
            name = filedialog.asksaveasfilename(initialdir=ROOT)
            if not name: return
            self.current = Path(name).resolve()
        if ROOT not in self.current.parents:
            messagebox.showerror("Blocked", "Save is restricted to this repository."); return
        try:
            self.current.write_text(self.editor.get("1.0", "end-1c"), encoding="utf-8")
            self.write_log("Saved " + str(self.current.relative_to(ROOT)))
            self.refresh_tree()
        except OSError as exc: messagebox.showerror("Save failed", str(exc))

    def save_current(self):
        if self.current is not None and self.current.exists():
            self.current.write_text(self.editor.get("1.0", "end-1c"), encoding="utf-8")

    def build(self):
        self.save_current()
        code, output = command([sys.executable, "scripts/build.py"])
        self.write_log("$ python scripts/build.py\n" + output)
        self.write_log("BUILD " + ("PASSED" if code == 0 else "FAILED"))

    def lint(self):
        self.save_current()
        for args in ([sys.executable, "scripts/menu_lint.py"], [sys.executable, "scripts/config_lint.py"]):
            code, output = command(list(args))
            self.write_log("$ " + " ".join(args) + "\n" + output)
            if code:
                self.write_log("LINT FAILED"); return
        self.write_log("LINT PASSED")

    def run_qemu(self):
        self.save_current()
        if not shutil.which("qemu-system-i386"):
            self.write_log("QEMU not found. Install qemu-system-i386 first."); return
        code, output = command([sys.executable, "scripts/build.py"])
        self.write_log(output)
        if code: self.write_log("Build failed; QEMU not started."); return
        code, output = command(["make", "image"])
        self.write_log(output)
        if code: self.write_log("Image build failed; QEMU not started."); return
        subprocess.Popen(["qemu-system-i386", "-drive", f"file={ROOT / 'build/floppy.img'},if=floppy,format=raw", "-boot", "a"], cwd=ROOT)
        self.write_log("QEMU launched with build/floppy.img")

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--build", action="store_true")
    parser.add_argument("--lint", action="store_true")
    args = parser.parse_args()
    if args.build:
        code, output = command([sys.executable, "scripts/build.py"]); print(output, end=""); return code
    if args.lint:
        for script in ("scripts/menu_lint.py", "scripts/config_lint.py"):
            code, output = command([sys.executable, script]); print(output, end="")
            if code: return code
        return 0
    IDE().mainloop()
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
