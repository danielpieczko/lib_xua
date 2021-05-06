# Copyright 2015-2021 XMOS LIMITED.
# This Software is subject to the terms of the XMOS Public Licence: Version 1.


def genstrings(outputChanCount, chanString, portString, structureString, adc_dac):
    
    for i in range(1,outputChanCount):

        print "#if (NUM_USB_CHAN_{c} > {i}-1)\n\
    .{s}ChanStr_{i}          = \"\"\n\
    #if ({i} < I2S_CHANS_{adcdac}+1)\n\
        \"Analogue {i}\"\n\
    #endif\n\
    #if (({i} < SPDIF_{p}_INDEX+2+1) && ({i} > SPDIF_{p}_INDEX)) && (XUA_SPDIF_{p}_EN)\n\
        #if ({i} < I2S_CHANS_{adcdac}+1)\n\
        \"/\"\n\
        #endif\n\
        #if({i} - SPDIF_{p}_INDEX == 1)\n\
            \"SPDIF 1\"\n\
        #elif({i} - SPDIF_{p}_INDEX == 2)\n\
            \"SPDIF 2\"\n\
        #endif\n\
    #endif\n\
    #if (({i} < ADAT_{p}_INDEX+8+1) && ({i} > ADAT_{p}_INDEX)) && defined(ADAT_{p})\n\
        #if (({i} < SPDIF_{p}_INDEX+2+1) && ({i} > SPDIF_{p}_INDEX)) && (XUA_SPDIF_{p}_EN) || ({i} < I2S_CHANS_{adcdac}+1)\n\
        \"/\"\n\
        #endif\n\
        #if({i} - ADAT_TX_INDEX == 1)\n\
            \"ADAT 1\"\n\
        #elif({i} - ADAT_TX_INDEX == 2)\n\
            \"ADAT 2\"\n\
        #elif({i} - ADAT_TX_INDEX == 3)\n\
            \"ADAT 3\"\n\
        #elif({i} - ADAT_TX_INDEX == 4)\n\
            \"ADAT 4\"\n\
        #elif({i} - ADAT_TX_INDEX == 5)\n\
            \"ADAT 5\"\n\
        #elif({i} - ADAT_TX_INDEX == 6)\n\
            \"ADAT 6\"\n\
        #elif({i} - ADAT_TX_INDEX == 7)\n\
            \"ADAT 7\"\n\
        #elif({i} - ADAT_TX_INDEX == 8)\n\
            \"ADAT 8\"\n\
        #endif\n\
     #endif\n\
        ,\n#endif\n".format(i=i, c=chanString, p=portString, s=structureString, adcdac=adc_dac);
    return;

print "/* AUTOGENERATED using chanstringgen.py */\n"
print "/* Not very nice looking but the standard preprocessor is not very powerful\n and we save some memory over doing this all at runtime */"

print "/* Output Strings */\n\n"

genstrings(33, "OUT", "TX", "output", "DAC");

print "/* Input Strings */\n\n"

genstrings(33, "IN", "RX", "input", "ADC");
