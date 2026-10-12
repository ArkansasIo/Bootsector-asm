# Object-Oriented Assembly (Pseudo-OOP)

## What OOP means in assembly
NASM has no built-in classes, inheritance, constructors, or garbage collection. An assembly project can use OOP-like conventions:
- fixed memory layouts (structures),
- one data block per object instance,
- routines that accept an instance pointer,
- method tables containing code pointers,
- explicit initialization and lifetime management,
- documented calling conventions.

## Example object
The file examples/oop_counter.asm defines a Counter structure with two 16-bit fields: value and step. Counter_increment receives the instance address in BX and updates the object. This is a method-by-convention, not a language-level member function.

## Method table pattern
A method table can be a sequence of near pointers. An object stores a pointer to the table. A call sequence loads the table pointer and calls a method address. Ensure code and data share the expected segment; use far pointers when methods cross segments.

Example layout:

~~~text
Object
+0: vtable pointer (word)
+2: state field (word)
+4: flags (byte)
~~~

## Encapsulation
Assembly cannot enforce private fields. Use naming conventions:
- Public API: Counter_init, Counter_increment, Counter_get
- Internal helpers: Counter__internal_*
- State: object-prefixed labels or structure offsets

## Inheritance and interfaces
Prefer composition for small real-mode systems. Interfaces can be represented as a table of routine pointers. Document which registers each method may clobber.

## Safety rules
- Validate object pointers and buffer bounds where practical.
- Preserve registers promised by the ABI.
- Avoid recursion in a tiny stack.
- Keep object and method table within reachable segment limits.
- STRUC defines offsets; ISTRUC instantiates actual data.

## Build
~~~sh
nasm -f bin examples/oop_counter.asm -o build/oop-counter.bin
~~~
