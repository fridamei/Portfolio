-- Fridamei


library IEEE;
use IEEE.std_logic_1164.all;
use IEEE.numeric_std.all;
 
entity pulse_width_modulator is 
	generic (
		constant mclk_cnt_max : integer := 197 -- Length larger than to 157 to achieve PWM frequency of 5 kHz or below, see calculations in report
		
	);
	port(
		mclk : in std_logic;
		reset : in std_logic;
		duty_cycle : in std_logic_vector(7 downto 0); -- 8 bits two's complement, first bit is a sign bit, so range is -128 to 127
		
		dir : out std_logic; -- Sets direction of the motor; 1 = forward, 0 = reverse
		en : out std_logic
		);
end pulse_width_modulator;
	
-- State machine architecture according to ASM-diagram
architecture rtl of pulse_width_modulator is
	type state_type is (forward_idle, forward, reverse_idle, reverse);
	signal present_state, next_state : state_type;
	
	signal pwm : std_logic; -- Temporary signal to get the right pwm-frequency
	
	signal mclk_cnt : integer := 0;   -- Clock counter
	signal pwm_cnt : unsigned(6 downto 0) := (others => '0'); -- Explanation in report 
	
	signal pwm_cnt_max : unsigned(pwm_cnt'length-1 downto 0) := unsigned(to_signed(-2, pwm_cnt'length)); -- The second highest value of the pwm_cnt given its length. Explanation below when used
	
begin
	
	-- Two processes, a clock counter and a PWM-counter, to set pwm high for the correct fraction of each periode (which have a frequency of 5 kHz or lower)
	
	CLK_CNT_PROCESS: process(mclk, reset)
	begin
		if reset then 
			mclk_cnt <= 0;
		elsif rising_edge(mclk) then
			if mclk_cnt < mclk_cnt_max-1 then -- Increment the mclk counter until it reaches the maximum value to achieve the chosen PWM frequency
				mclk_cnt <= mclk_cnt + 1;
			else
				mclk_cnt <= 0; -- Wraps the counter
			end if;
		end if;
	end process; 
	
	
	
	PWM_PROCESS: process(mclk, reset)
	begin
		if reset then
			pwm_cnt <= (others => '0');
			pwm <= '0';
		elsif rising_edge(mclk) then
			if mclk_cnt = 0 then
				pwm_cnt <= pwm_cnt + 1;
				pwm <= '0'; -- Ensures the pwm also has a correct low-periode. Is overridden in if-test below if pwm should still be high according to duty_cycle
				 -- If the pwm counter reached its second highest value, start over from zero. 
				 -- Second highest because we do not want the pwm_cnt to reach the same value as duty cycle because
				 -- if the duty_cycle is set to its maximum value, we want a 100 % duty, 
				 -- but if the pwm_count is equal to abs(duty_cycle), the enable will be off for the clock periode they correspond before the pwm_count wraps
				if pwm_cnt = pwm_cnt_max then
					pwm_cnt <= (others => '0');
				end if;
	
				if pwm_cnt < unsigned(abs(signed(duty_cycle))) then -- convert to unsigned to compare
					pwm <= '1';
				end if;
			end if;
		end if;
	end process; 


-- Processes describing the actual PWM state machine

	-- 1: sequential state assignment
	present_state <=
		reverse_idle when reset else -- Asynchronous reset
		next_state when rising_edge(mclk);
		
	-- 2: combinational next_state logic. Updates the next_state when triggered by changes in the duty_cycle or present_state
	-- The dir will never be changed while en is high as change in duty_cycle from positive to negative or vice versa will put us in a intermediate idle state where en is low to change the dir
	NEXT_STATE_CL: process(duty_cycle, present_state) is
	begin
		case present_state is
			-- When in the reverse_idle-state:
			when reverse_idle => 
				next_state <=
					reverse when to_integer(signed(duty_cycle)) < 0 else forward_idle; 
			
			-- When in the reverse-state:
			when reverse =>
				next_state <= 
					reverse when to_integer(signed(duty_cycle)) < 0 else reverse_idle;
					
			-- When in the forward_idle-state:
			when forward_idle =>
				next_state <=
					forward when to_integer(signed(duty_cycle)) > 0 else reverse_idle;
					
			-- When in the forward-state:
			when forward =>
				next_state <= 
					forward when to_integer(signed(duty_cycle)) > 0 else forward_idle;
					
		end case;
	end process NEXT_STATE_CL;
		
		
	-- 3: combinational output logic
	-- The outputs change as soon as any of the reliances change given the state we're in
	OUTPUT_CL: process(all) is
	begin
		-- Default output values
		dir <= '0';
		en <= '0';
		
		-- State based assignment
		case present_state is
			when reverse_idle =>
				en  <= '0';
				dir <= '0';
			
			when reverse =>
				en <= pwm;
				dir <= '0';
				
			when forward_idle =>
				en <= '0';
				dir <= '1';
				
			when forward =>
				en <= pwm;
				dir <= '1';
		end case;
	end process OUTPUT_CL;		
end rtl;				