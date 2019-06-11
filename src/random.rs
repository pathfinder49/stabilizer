// 32-bit XOR PRNG
pub struct Prng {
    state: u32,
    seed: u32,
}

impl Prng {
    pub const fn new(seed: u32) -> Self {
        Self {
            state: seed,
            seed: seed,
        }
    }

    pub fn reset(self: &mut Self) {
        self.state = self.seed
    }

    pub fn next(self: &mut Self) -> u32 {
        self.state ^= self.state << 13;
        self.state ^= self.state >> 17;
        self.state ^= self.state << 5;
        self.state
    }
}
