import os

# toolchains options
ARCH='arm'
CPU='cortex-m4'
CROSS_TOOL='gcc'

if os.getenv('RTT_CC'):
    CROSS_TOOL = os.getenv('RTT_CC')

# cross_tool provides the cross compiler
# EXEC_PATH is the compiler execute path, for example, CodeSourcery, Keil MDK, IAR

if  CROSS_TOOL == 'gcc':
    PLATFORM    = 'gcc'
    EXEC_PATH   = r'.'
elif CROSS_TOOL == 'keil':
    PLATFORM    = 'armcc'
    EXEC_PATH   = 'C:/Keil_v5'
elif CROSS_TOOL == 'iar':
    print('================ERROR============================')
    print('Not support iar yet!')
    print('=================================================')
    exit(0)

if os.getenv('RTT_EXEC_PATH'):
    EXEC_PATH = os.getenv('RTT_EXEC_PATH')

BUILD = 'debug'

if PLATFORM == 'gcc':
    # toolchains
    PREFIX = 'arm-none-eabi-'
    CC = PREFIX + 'gcc'
    AS = PREFIX + 'gcc'
    AR = PREFIX + 'ar'
    CXX = PREFIX + 'g++'
    LINK = PREFIX + 'gcc'
    TARGET_EXT = 'elf'
    SIZE = PREFIX + 'size'
    OBJDUMP = PREFIX + 'objdump'
    OBJCPY = PREFIX + 'objcopy'

    DEVICE = ' -mcpu=cortex-m4 -mthumb'
    CFLAGS = DEVICE
    AFLAGS = ' -c' + DEVICE + ' -x assembler-with-cpp'
    LFLAGS = DEVICE + ' -Wl,--gc-sections,-Map=rtthread.map,-cref,-u,Reset_Handler -T board/linker_scripts/link.lds'

    CPATH = ''
    LPATH = ''

    if BUILD == 'debug':
        CFLAGS += ' -O0 -gdwarf-2'
        AFLAGS += ' -gdwarf-2'
    else:
        CFLAGS += ' -O2'
        
    CXXFLAGS = CFLAGS 

    POST_ACTION = OBJCPY + ' -O ihex $TARGET rtthread.hex\n' + SIZE + ' $TARGET \n'

elif PLATFORM == 'armcc':
    # toolchains
    CC = 'armcc'
    AS = 'armasm'
    AR = 'armar'
    LINK = 'armlink'
    TARGET_EXT = 'axf'

    DEVICE = ' --cpu Cortex-M4.fp'
    CFLAGS = '-c ' + DEVICE + ' --apcs=interwork --c99'
    AFLAGS = DEVICE + ' --apcs=interwork '
    LFLAGS = DEVICE + ' --info sizes --info totals --info unused --info veneers --list rt-thread.map --strict --scatter "board\linker_scripts\link.sct"'

    CFLAGS += ' -D__MICROLIB '
    AFLAGS += ' --pd "__MICROLIB SETA 1" '
    LFLAGS += ' --library_type=microlib '
    EXEC_PATH += '/ARM/ARMCC/bin/'

    if BUILD == 'debug':
        CFLAGS += ' -g -O0'
        AFLAGS += ' -g'
    else:
        CFLAGS += ' -O2'

    POST_ACTION = 'fromelf --bin $TARGET --output rtthread.bin \nfromelf -z $TARGET'
    
elif PLATFORM == 'iar':
    # toolchains
    CC = 'iccarm'
    CXX = 'iccarm'
    AS = 'iasmarm'
    AR = 'iarchive'
    LINK = 'ilinkarm'
    TARGET_EXT = 'out'

    DEVICE = '-Dewarm'

    CFLAGS = DEVICE
    CFLAGS += ' --diag_suppress Pa050'
    CFLAGS += ' --no_cse'
    CFLAGS += ' --no_unroll'
    CFLAGS += ' --no_inline'
    CFLAGS += ' --no_code_motion'
    CFLAGS += ' --no_tbaa'
    CFLAGS += ' --no_clustering'
    CFLAGS += ' --no_scheduling'
    CFLAGS += ' --endian=little'
    CFLAGS += ' --cpu=Cortex-M4'
    CFLAGS += ' -e'
    CFLAGS += ' --fpu=VFPv4_sp'
    CFLAGS += ' --dlib_config "' + EXEC_PATH + '/arm/INC/c/DLib_Config_Normal.h"'
    CFLAGS += ' --silent'

    AFLAGS = DEVICE
    AFLAGS += ' -s+'
    AFLAGS += ' -w+'
    AFLAGS += ' -r'
    AFLAGS += ' --cpu Cortex-M4'
    AFLAGS += ' --fpu VFPv4_sp'
    AFLAGS += ' -S'

    if BUILD == 'debug':
        CFLAGS += ' --debug'
        CFLAGS += ' -On'
    else:
        CFLAGS += ' -Oh'

    LFLAGS = ' --config "board/linker_scripts/link.icf"'
    LFLAGS += ' --entry __iar_program_start'

    CXXFLAGS = CFLAGS
    
    EXEC_PATH = EXEC_PATH + '/arm/bin/'
    POST_ACTION = 'ielftool --bin $TARGET rtthread.bin'
