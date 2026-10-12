# UI Structure

## Main menu
- Boot and loader options
- Disk tools and image options
- Modules and submodules
- System information and diagnostics
- Help and keyboard controls
- Reboot

## Navigation tree
Main
- Boot options -> Stage 1, Stage 2, load address
- Disk tools -> geometry, image layout, clone/verify (future)
- Modules -> Core, UI, DiskServices, Diagnostics
- Diagnostics -> boot report, memory map (planned)
- Help -> controls, limitations

## UI state contract
- `active_menu`: current menu ID
- `previous_menu`: return destination
- `selected_index`: selected menu index if arrow navigation is implemented
- `input_key`: latest BIOS keyboard input
- `status_message`: result/error text

Current assembly uses numeric keys and B/Backspace/Escape. Arrow navigation and indexed menu tables are planned.
