-- Fridamei

library IEEE;
use IEEE.std_logic_1164.all;
use IEEE.numeric_std.all;

entity quadrature_decoder is
	port (
	reset : in std_logic;
	mclk : in std_logic;
	sa : in std_logic;
	sb : in std_logic;

	pos_inc : out std_logic; 
	pos_dec : out std_logic
	);
end; 

architecture rtl of quadrature_decoder is
	type state_type is (s_reset, s_init, s0, s1, s2, s3);
	signal present_state, next_state : state_type; -- Dette initialiserer present_state til s_reset, tror next_state også blir det uten at det egentlig har noe å si
	
	signal inc, dec, err : std_logic;

begin
	-- 1: sequential state assignment
	present_state <=
		s_reset when reset = '1' else -- Asynchronous reset
		next_state when rising_edge(mclk);
	
	pos_inc <= '0' when reset else inc when rising_edge(mclk);
	pos_dec <= '0' when reset else dec when rising_edge(mclk);
		
	-- 2: combinational next_state logic. Updates the next_state when triggered by changes in the duty_cycle or present_state
	-- The dir will never be changed while en is high as change in duty_cycle from positive to negative or vice versa will put us in a intermediate idle state where en is low to change the dir
	
	-- Denne trigger også når present_state endrer seg, det skjer ved rising edge. 
	NEXT_STATE_CL: process(present_state, sa, sb) is
	begin
		-- Default values to ensure pos_inc and pos_dec are only high for one clock periode
		inc <= '0';
		dec <= '0';
		err <= '0';
		
		case present_state is
			-- When in S_reset
			when s_reset =>
				next_state <= s_init;
				
			-- When in S_init
			when s_init => 
				next_state <=
					s0 when not sa and not sb else
					s1 when not sa and sb else
					s2 when sa and sb else
					s3 when sa and not sb; 
					
			-- When in s0	
			when s0 => 
				if not sa and not sb then
					next_state <= s0;
				elsif not sa and sb then
					next_state <= s1;
					inc <= '1';
				elsif sa and not sb then
					next_state <= s3;
					dec <= '1';
				elsif sa and sb then
					next_state <= s_reset;
					err <= '1';
				end if;
				
			-- When in s1
			when s1 => 
				if not sa and not sb then
					next_state <= s0;
					dec <= '1';
				elsif not sa and sb then
					next_state <= s1;
				elsif sa and not sb then
					next_state <= s_reset;
					err <= '1';
				elsif sa and sb then
					next_state <= s2;
					inc <= '1';
				end if;
				
			-- When in s2	
			when s2 => 
				if not sa and not sb then
					next_state <= s_reset;
					err <= '1';
				elsif not sa and sb then
					next_state <= s1;
					dec <= '1';
				elsif sa and not sb then
					next_state <= s3;
					inc <= '1';
				elsif sa and sb then
					next_state <= s2;
				end if;
			
			-- When in s3
			when s3 => 
				if not sa and not sb then
					next_state <= s0;
					inc <= '1';
				elsif not sa and sb then
					next_state <= s_reset;
					err <= '1';
				elsif sa and not sb then
					next_state <= s3;
				elsif sa and sb then
					next_state <= s2;
					dec <= '1';
				end if;
		end case;
	end process NEXT_STATE_CL;
end rtl;