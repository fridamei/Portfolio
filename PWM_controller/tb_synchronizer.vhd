-- Fridamei

library IEEE;
use IEEE.std_logic_1164.all;
use IEEE.numeric_std.all;

entity tb_synchronizer is
end entity;

architecture bhv of tb_synchronizer is 
	signal reset : std_logic := '1';
	signal mclk : std_logic := '0';

	signal dir, en : std_logic := '0';
	signal synced_dir, synced_en : std_logic;
	signal duty_cycle : std_logic_vector(7 downto 0); -- Fra selvtest til PWM, hvor den blir oversatt til dir- og en-signaler
	
	constant half_periode : time := 5 ns; -- Clock frequency 100 MHz, same as oscillator on board
	constant clk_freq : integer := 636; -- With clk_freq = 10 each second will be scaled down 1e7 times and thus be modelled as 100 ns. Nå 1000 ns, gjør nyw beregninger
	
	constant mclk_cnt_max : integer := 5;

begin
	UNIT_STM: entity work.self_test_module(rtl) 
		generic map(
			clk_freq => clk_freq
		)
		
		port map (
			mclk => mclk, 
			reset => reset,
			duty_cycle => duty_cycle
		);
		
	UNIT_PWM: entity work.pulse_width_modulator(rtl)
		generic map (
			mclk_cnt_max => mclk_cnt_max
		)
		port map (
			mclk => mclk, 
			reset => reset,
			duty_cycle => duty_cycle,
			dir => dir,
			en => en
		);
	
	DUT_SYNC: entity work.synchronizer(rtl)
		port map (
			mclk => mclk,
			reset => reset,
			async_a => dir,
			async_b => en,
			
			synced_a => synced_dir,
			synced_b => synced_en
		);

	mclk <= not mclk after half_periode;
	reset <= '0' after 10 ns;
	
end bhv; 