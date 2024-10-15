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

1. I'm just out of college, not many prospects at the moment for technical work, so I may as well knock out a relatively simple project.
2. I'm interested in malware analysis, and assembly is an important skill for that kind of work, and writing an assembler will give me a pretty confident knowledge of x86 assembly.
3. I will gain knowledge of the inner details of the ELF and PE file formats, also quite valuable information.
4. I would like to *write* some assembly, and while NASM and other options are mature and well-featured, I think there's room for an easy to use Rust tool. I also like to make my own tools when I can; tools that work the way I think they ought to work and are documented according to my own preferences.
5. Getting more comfortable with Rust is a plus.

I began by asking Claude, "Help me get started writing an assembler", which I am not ashamed to admit. AI is a tool, and so far it's just been a shortcut around reading a lot of vague information on how exactly assemblers work, though after the initial work I will have no choice but to dive into the x86 Developer Manual (a massive tome). Claude also isn't really capable of doing all the work for me. It can give me obvious ideas, such as writing a proper tokenizer instead of a string-splitting approach, and it can answer Rust syntax questions, but it can't understand the code for me, and if I can't understand it I can't debug it, and Claude isn't smart enough to debug for me. So my learning and understanding isn't really impeded by using AI, so far at least.

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

Anyway, there's not much else to tell in this first post. The code so far is only a few files. At a good pace it shouldn't take very long to get it to a working state.