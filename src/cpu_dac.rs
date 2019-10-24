use serde::{Serialize, Deserialize};


#[derive(Copy,Clone,Deserialize,Serialize)]
pub struct CPU_DAC {
    pub out: u32,  // making this u16 breaks spi interrupt loop
    pub en: bool,
}

#[allow(unused)]
impl CPU_DAC {
    pub fn set_scale_out(&mut self, out: f32) -> Result<(), &str> {
        // out 0 -> 1
        self.out = (out * (0xfff as f32)) as u32;
        Ok(())
    }

    pub fn get_scale_out(&self) -> Result<f32, &str> {
        Ok( (self.out as f32) / (0xfff as f32))
    }

    pub fn set_en(&mut self, enable: bool) -> Result<(), &str> {
        self.en = enable;
        Ok(())
    }
    pub fn get_en(&mut self, enable: bool) -> Result<bool, &str> {
        Ok(self.en as bool)
    }

}
