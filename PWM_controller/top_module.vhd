-- Fridamei

library IEEE;
use IEEE.std_logic_1164.all;
use IEEE.numeric_std.all;

entity top_module is
	port(
		-- System inputs
		signal mclk : in std_logic; -- Connected to 100 MHz oscillator on board
		signal reset : in std_logic;
		
		-- Inputs from the Quadrature encoder
		signal sa : in std_logic;
		signal sb : in std_logic;
	
		-- Outputs to the motor
		signal en_synch : out std_logic;
		signal dir_synch : out std_logic;
		
		-- Outputs to the seven segment display
		signal c : out std_logic;
		signal abcdefg : out std_logic_vector(6 downto 0)
	);
end entity;

architecture structural of top_module is
	-- Clock constants
	constant clkHz : integer := 1e8; -- 100 MHz (10 Hz for more visibility in testing)
	
	-- PWM, self_test_module
	signal duty_cycle : std_logic_vector(7 downto 0) := (others => '0'); -- Kommer som output fra self_test_module og sendes inn i PWM
	signal dir : std_logic := '0';
	signal en : std_logic := '0';

	-- Synchronized input from the Quadrature encoder
	signal ff1a : std_logic := '0';
	signal ff1b : std_logic := '0';
	signal sa_synch : std_logic := '0';
	signal sb_synch : std_logic := '0';
	
	-- Outputs from the quadrature encoder
	signal pos_inc : std_logic := '0';
	signal pos_dec : std_logic := '0';
	
	-- Outputs from the velocity reader
	signal velocity : signed(7 downto 0) := (others => '0');
	
	-- Self-test module
	component self_test_module is
		port (
			mclk : in std_logic; -- Connected to 100 MHz oscillator on board
			reset : in std_logic;
			duty_cycle : out std_logic_vector(7 downto 0)
		);
	end component;

	-- PWM declaration 
	component pulse_width_modulator is
		port (
			mclk : in std_logic; --100MHz oscillator on zedboard 
			reset : in std_logic; 
			duty_cycle : in std_logic_vector(7 downto 0); -- 8 bits two's complement, first bit is a sign bit, so range is -128 to 127
		
			dir : out std_logic;
			en : out std_logic
		);
	end component;
	
	-- Quadrature decoder
	component quadrature_decoder is
		port (
			reset : in std_logic;
			mclk : in std_logic;
			sa : in std_logic;
			sb : in std_logic;

			pos_inc : out std_logic; 
			pos_dec : out std_logic
		);
	end component;
	
	-- Velocity reader
	component velocity_reader is
		port (
			mclk      : in std_logic; 
			reset     : in std_logic; 
			pos_inc   : in std_logic;
			pos_dec   : in std_logic;
			velocity  : out signed(7 downto 0)
		);
	end component;
		
	-- Seven segment display
	component seg7ctrl is 
		port (
			mclk : in std_logic; 
			reset : in std_logic;
			velocity : in signed(7 downto 0);
		
			abcdefg : out std_logic_vector(6 downto 0);
			c : out std_logic
		);
	end component;
	
	
	-- Concurrent statements 
begin 
	
	UNIT_QUAD_DEC: entity work.quadrature_decoder(rtl)
		port map (
			mclk => mclk,
			reset => reset,
			
			sa => sa_synch,
			sb => sb_synch,

			pos_inc => pos_inc,
			pos_dec => pos_dec
		);
	
	UNIT_VEL_READER: entity work.velocity_reader(rtl)
		port map (
			mclk => mclk,
			reset => reset,
			
			pos_inc => pos_inc,
			pos_dec => pos_dec,
			velocity  => velocity
		);
	
	UNIT_SEG7CTRL: entity work.seg7ctrl(rtl)
		port map (
			mclk => mclk,
			reset => reset,
			velocity  => velocity,
		
			abcdefg => abcdefg,
			c => c
		);
	
	UNIT_STM: entity work.self_test_module(rtl)
	port map (
		mclk => mclk,
		reset => reset,
		duty_cycle => duty_cycle -- Outputs the duty_cycles read from ROM, one every third seconds
	);
		
	UNIT_PWM: entity work.pulse_width_modulator(rtl) 
    port map (
		-- Inputs
		mclk => mclk,
		reset => reset,
		duty_cycle => duty_cycle,
		
		-- Outputs
		dir => dir,
		en => en -- Outputs en and dir, to be fed into the synchronizers 
    );    
	
	INP_SYNC: 
	ff1a <= '0' when reset else sa when rising_edge(mclk);
	ff1b <= '0' when reset else sb when rising_edge(mclk);
	sa_synch <= '0' when reset else ff1a when rising_edge(mclk);
	sb_synch <= '0' when reset else ff1b when rising_edge(mclk);
	
	OUT_SYNC:
	dir_synch <= '0' when reset else dir when rising_edge(mclk);
	en_synch <= '0' when reset else en when rising_edge(mclk);
	
end structural;