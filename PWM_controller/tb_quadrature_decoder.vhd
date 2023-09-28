-- Fridamei

library IEEE;
use IEEE.std_logic_1164.all;
use IEEE.numeric_std.all;

entity tb_quadrature_decoder is
end entity;

architecture bhv of tb_quadrature_decoder is
	signal reset : std_logic := '0';
	signal mclk : std_logic := '0';
	signal sa : std_logic := '0';
	signal sb : std_logic := '0';

	signal pos_inc : std_logic; 
	signal pos_dec : std_logic;
	
	constant half_period : time := 5 ns;
	constant period : time := 2*half_period;
	
begin
	DUT_DECODER: entity work.quadrature_decoder(rtl)
		port map (
			reset => reset,
			mclk => mclk,
			sa => sa,
			sb => sb,
	
			pos_inc => pos_inc,
			pos_dec => pos_dec
		);
		
	-- Genererer klokkesignal 
	mclk <= not mclk after half_period;

	
	STIMULI: process is
	begin
		reset <= '1', '0' after 100 ns;
		wait for 100 ns;
		
		-- Testing the forward motion where the sa leads the sb by 1/4 of a PWM period. 
		-- The pos_dec should go high when transitioning
		
		-- The FSM is currently in s_init. 
		-- When sa goes high, the FSM transitions from s_init to s3. 
		-- Neither pos_dec or pos_inc should go high at this point
		sa <= '1', '0' after 12*period;
		assert not pos_dec and not pos_inc
			report "Pos_dec or pos_inc goes high, check transition from S_init to S3 in FSM";
		report "Transition from S_init to S3 OK";
		
		wait for 6*period;
		sb <= '1', '0' after 12*period;
		-- When sb goes high, the FSM transitions from S3 to S2 and pos_dec goes high for one clock cycle
		wait until mclk'stable and mclk = '1';
		assert pos_dec
			report "Transition from S3 to S2 does not generate pos_dec";
		wait until mclk'stable and mclk = '1';
		assert not pos_dec
			report "Pos_dec high for longer than 1 clock period";
		report "Transition from S3 to S2 OK";
		
		-- When sa goes low again, the fsm should transition from S2 to S1 and set pos_dec high for one clock cycle
		wait until not sa;
		wait until mclk'stable and mclk = '1'; 
		assert pos_dec
			report "Transition from S2 to S1 does not generate pos_dec";
		wait until mclk'stable and mclk = '1';
		assert not pos_dec
			report "Pos_dec high for longer than 1 clock period";
		report "Transition from S2 to S1 OK";
		
		-- When sb goes low again, the fsm should transition from S1 to S0 and set pos_dec high for one clock cycle
		wait until not sb;
		wait until mclk'stable and mclk = '1'; 
		assert pos_dec
			report "Transition from S1 to S0 does not generate pos_dec";
		wait until mclk'stable and mclk = '1';
		assert not pos_dec
			report "Pos_dec high for longer than 1 clock period";
		report "Transition from S1 to S0 OK";
		
		report "Forward testing done, starting backward testing";
		
		
		-- Testing the backwards motion where sb leads sa and pos_inc should go high
		
		-- Reset to put the FSM in S_reset
		reset <= '1', '0' after 100 ns;
		wait for 105 ns;
		
		-- Transition from S_init to S1
		sb <= '1', '0' after 12*period;
		assert not pos_dec and not pos_inc
			report "Pos_dec or pos_inc goes high, check transition from S_init to S1 in FSM";
		report "Transition from S_init to S1 OK";
		
		wait for 6*period;
		sa <= '1', '0' after 12*period;
	
		-- When sa goes high, the FSM transitions from S1 to S2 and pos_inc goes high for one clock cycle
		wait until mclk'stable and mclk = '1';
		assert pos_inc
			report "Transition from S1 to S2 does not generate pos_inc";
		wait until mclk'stable and mclk = '1';
		assert not pos_inc
			report "Pos_inc high for longer than 1 clock period";
		report "Transition from S1 to S2 OK";
		
		
		-- Transition from S2 to S3
		wait until not sb;
		wait until mclk'stable and mclk = '1'; 
		assert pos_inc
			report "Transition from S2 to S3 does not generate pos_inc";
		wait until mclk'stable and mclk = '1';
		assert not pos_inc
			report "Pos_inc high for longer than 1 clock period";
		report "Transition from S2 to S3 OK";
		
		-- When sa goes low again, the FSM should transition from S3 to S0 and set pos_inc high for one clock cycle
		wait until not sa;
		wait until mclk'stable and mclk = '1'; 
		assert pos_inc
			report "Transition from S3 to S0 does not generate pos_inc";
		wait until mclk'stable and mclk = '1';
		assert not pos_inc
			report "Pos_inc high for longer than 1 clock period";
		report "Transition from S3 to S0 OK";
		
		report "Backward testing done";
		wait for 12*period;
		std.env.stop;
	end process;
end bhv; 