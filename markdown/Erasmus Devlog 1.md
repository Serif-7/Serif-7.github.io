---
tags:
  - devlog
  - assembly
  - rust
published: October 15, 2024
updated: Never
draft: false
---

Commit at time of writing: https://github.com/Serif-7/erasmus/tree/54243c956df428727a7939eb763bd3bb282df800

I've begun work on a Rust x86_64 assembler that I am calling **Erasmus**. I'm doing this for a few reasons:

1. I'm interested in malware analysis, and reading assembly is an important skill for that kind of work. As such, writing an assembler seems like an efficient way to acquire a confident knowledge of x86 assembly.
2. I will gain knowledge of the inner details of the ELF and PE file formats, also quite valuable information.
3. I would like to *write* some assembly, and while NASM and other options are mature and well-featured, I think there's room for an easy to use Rust tool. I also like to make my own tools when I can; tools that work the way I think they ought to work and are documented according to my own preferences.
4. Getting more comfortable with Rust is a plus.

I started by writing a simple tokenizer. I did several advent of code problems over the summer and I learned that tokenizing is always helpful when processing regular string input. Because this isn't a compiler I thankfully don't need anything complicated; assembly instructions are just mnemonics for machine code, so the basic problem is simple. Complexity will come if I decide to add macro-assembler features later.

Detailed information about how assemblers work is somewhat scarce online. I suppose it's a relatively esoteric activity these days, so that makes sense. Since I'm just working on parsing and encoding at the moment, no domain knowledge is needed. After the initial work is done I will have no choice but to dive into the x86 Developer Manual (a massive tome).

The tokenizer is pretty much complete, and converts an assembly program into a list of tokens of the following type:

```rust
#[derive(Debug, PartialEq)]
pub enum Token {
    Label(String),
    Instruction(String),
    Register(String),
    Number(i64),
    String(String),
    Comma,
    OpenBracket,
    CloseBracket,
    Plus,
    Minus,
    Mult,
    Identifier(String),
}
```

The assembler struct will operate on lists of these tokens. I've written some very, very preliminary encoding logic, which looks like this:

```rust
fn encode_instruction(token: &tokenizer::Token) -> Option<u8> {
    match token {
        tokenizer::Token::Instruction(instr) => match instr.as_str() {
            "mov" => Some(0x88),
            "add" => Some(0x01),
            "sub" => Some(0x29),
            "push" => Some(0x50),
            "pop" => Some(0x58),
            _ => None,  // Unknown instruction
        },
        _ => None,  // Not an instruction token
    }
}
```

Quite simple, though it probably shouldn't return an `Option`. If anything *but* an instruction token is going into that function, something is terribly wrong.

Anyway, there's not much else to tell in this first post. The code so far is only a few files. At a good pace it shouldn't take very long to get it to a working state. My next task is to finish and test the encoding logic for the basic instructions like `mov` and `add`, and as quickly as possible get the program to a point where it can output executable files.