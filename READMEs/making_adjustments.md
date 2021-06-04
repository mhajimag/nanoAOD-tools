# Making adjustments for your process

As described in [underlying principles](underlying_principles.md), there may be cases where the LHEPart method of extracting the event information will not work. The [walkthrough example](walkthrough.md) was a case where using the LHEPart information worked. Here, we will go through the steps of reweighting ttH samples. This is a case where LHEPart does not work and GenPart will have to be used.



First let's use EFT2Obs to make a ttH reweighting module. Use this proc_card.dat:
```
import model SMEFTsim_U35_MwScheme_UFO

generate p p > h t t~ NP<=1

output ttH-SMEFTsim
```
and use the following commands to do the rest:
```
source env.sh
./scripts/setup_process.sh ttH-SMEFTsim
python scripts/make_config.py -p ttH-SMEFTsim -o config_SMEFT_STXS.json --pars SMEFT:6 \ 
--def-val 0.01 --def-sm 0.0 --def-gen 0.0
python scripts/make_param_card.py -p ttH-SMEFTsim -c config_SMEFT_STXS.json \ 
-o cards/ttH-SMEFTsim/param_card.dat
python scripts/make_reweight_card.py config_SMEFT_STXS.json cards/ttH-SMEFTsim/reweight_card.dat
./scripts/setup_process_standalone.sh ttH-SMEFTsim
python scripts/make_standalone.py -p ttH-SMEFTsim -o rw_ttH-SMEFTsim -c config_SMEFT_STXS.json \ 
--rw-dir MG5_aMC_v2_6_7/ttH-SMEFTsim-standalone
```

We will reweight this dataset:
```
/ttHJetToGG_M125_TuneCP5_13TeV-amcatnloFXFX-madspin-pythia8_storeWeights/RunIISummer19UL18NanoAODv2-106X_upgrade2018_realistic_v15_L1v1-v1/NANOAODSIM
```
and this file in particular:
```
/store/mc/RunIISummer19UL18NanoAODv2/ttHJetToGG_M125_TuneCP5_13TeV-amcatnloFXFX-madspin-pythia8_storeWeights/NANOAODSIM/106X_upgrade2018_realistic_v15_L1v1-v1/40000/3A2BC04C-E3DA-A142-A7DB-8421AA9C8BE2.root
```

First, let's run the reweighting with the LHE method and in the verbose mode and see what happens:
```
python scripts/run_reweighting.py path/to/output \
 root://xrootd-cms.infn.it//store/mc/RunIISummer19UL18NanoAODv2/ttHJetToGG_M125_TuneCP5_13TeV-amcatnloFXFX-madspin-pythia8_storeWeights/NANOAODSIM/106X_upgrade2018_realistic_v15_L1v1-v1/40000/3A2BC04C-E3DA-A142-A7DB-8421AA9C8BE2.root \
 path/to/rw_module -N 10 -v
```

<details>
<summary>Click here to see the output of this command.</summary>
<p>

```
[mknight@lxplus740 NanoAODTools]$ python scripts/run_reweighting.py .  root://xrootd-cms.infn.it//store/mc/RunIISummer19UL18NanoAODv2/ttHJetToGG_M125_TuneCP5_13TeV-amcatnloFXFX-madspin-pythia8_storeWeights/NANOAODSIM/106X_upgrade2018_realistic_v15_L1v1-v1/40000/3A2BC04C-E3DA-A142-A7DB-8421AA9C8BE2.root  ../../../../EFT2Obs/rw_ttH-SMEFTsim/ -N 10 -v
>> 1 parameters, 3 reweight points
>> LO Reweighting
>> Initialising modules...
>> StandaloneReweight class initialized
>> Accepted PDG lists:
   - [4, -4, 25, 6, -6]
   - [21, 21, 25, 6, -6]
   - [2, -2, 25, 6, -6]
   - [3, -1, 25, 6, -6]
   - [1, -3, 25, 6, -6]
   - [1, -1, 25, 6, -6]
   - [3, -3, 25, 6, -6]
Will write selected trees to .
Pre-select 10 entries out of 10 (100.00%)
>> Event with PDGs [2, -2, 25, 5, 2, -1, -5, 3, -4] does not match any known process
---------------------------------------------------------------------------
 Particle | status  | helicity |   | E       | P_x     | P_y     | P_z      
---------------------------------------------------------------------------
         u        -1         1          122.2       0.0       0.0     122.2
    anti-u        -1        -1         1034.5       0.0       0.0   -1034.5
    Higgs0         1         0          567.7      65.6      98.8    -540.9
         b         1        -1           48.2     -16.3      29.7     -34.3
         u         1        -1           75.7      -3.8     -75.5      -4.4
    anti-d         1         1           55.8      46.2     -17.4      26.0
    anti-b         1         1          247.8    -102.0       6.2    -225.8
         s         1        -1           91.8     -33.8     -26.7     -81.1
    anti-c         1         1           69.7      44.1     -15.0     -51.9
[1.0, 1.0, 1.0]
 
>> Event with PDGs [21, 21, 25, 5, 2, -1, -5, 3, -4, 21] does not match any known process
---------------------------------------------------------------------------
 Particle | status  | helicity |   | E       | P_x     | P_y     | P_z      
---------------------------------------------------------------------------
         g        -1         1          422.4       0.0       0.0     422.4
         g        -1        -1          570.0       0.0       0.0    -570.0
    Higgs0         1         0          268.3    -171.7    -152.1     -61.0
         b         1        -1          114.4     -90.2     -70.5       1.3
         u         1        -1           46.4     -19.9      41.9       0.8
    anti-d         1         1           64.5     -14.9     -12.6      61.5
    anti-b         1         1          199.1      66.7     163.6     -91.9
         s         1        -1           49.3      -6.8      30.0     -38.5
    anti-c         1         1           86.8      75.1      -7.0     -43.0
         g         1         1          163.5     161.7       6.6      23.3
[1.0, 1.0, 1.0]
 
>> Event with PDGs [21, 21, 25, 5, 4, -3, -5, 1, -2] does not match any known process
---------------------------------------------------------------------------
 Particle | status  | helicity |   | E       | P_x     | P_y     | P_z      
---------------------------------------------------------------------------
         g        -1        -1          332.7       0.0       0.0     332.7
         g        -1        -1          351.1       0.0       0.0    -351.1
    Higgs0         1         0          179.8       9.8     -48.1    -119.6
         b         1        -1          150.9     129.7      66.3     -39.3
         c         1        -1           49.4       7.5     -46.4      15.3
    anti-s         1         1           34.9       9.7      31.5     -11.7
    anti-b         1         1           62.9     -37.0      50.9      -0.2
         d         1        -1           40.3     -29.2     -27.8       1.1
    anti-u         1         1          165.4     -90.5     -26.3     136.0
[1.0, 1.0, 1.0]
 
>> Event with PDGs [21, 21, 25, 5, 2, -1, -5, -16, 15] does not match any known process
---------------------------------------------------------------------------
 Particle | status  | helicity |   | E       | P_x     | P_y     | P_z      
---------------------------------------------------------------------------
         g        -1         1          586.3       0.0       0.0     586.3
         g        -1         1          128.9       0.0       0.0    -128.9
    Higgs0         1         0          269.8       0.8       6.4     239.0
         b         1        -1           43.6     -43.6       1.1       1.1
         u         1        -1           43.7      37.5      -2.7      22.1
    anti-d         1         1          166.6      19.9      65.7     151.8
    anti-b         1         1           97.9     -63.2     -56.0      49.7
anti-nu_tau         1         1           35.2      13.5      17.7      27.2
      tau-         1        -1           58.4      35.1     -32.3     -33.6
[1.0, 1.0, 1.0]
 
>> Event with PDGs [21, 21, 25, 5, 16, -15, -5, 13, -14] does not match any known process
---------------------------------------------------------------------------
 Particle | status  | helicity |   | E       | P_x     | P_y     | P_z      
---------------------------------------------------------------------------
         g        -1        -1          302.6       0.0       0.0     302.6
         g        -1         1          468.2       0.0       0.0    -468.2
    Higgs0         1         0          137.5     -27.3     -27.4      42.1
         b         1        -1           61.8      22.9     -14.7      55.5
    nu_tau         1        -1          139.8      83.9     105.4      37.1
      tau+         1         1           59.1     -13.4      57.6      -0.3
    anti-b         1         1          221.3     -72.5     -34.6    -206.2
       mu-         1        -1           31.8      20.5       8.7     -22.6
anti-nu_mu         1         1          119.5     -14.2     -95.0     -71.2
[1.0, 1.0, 1.0]
 
>> Event with PDGs [21, 1, 25, 5, 12, -11, -5, 1, -4, 1, 21] does not match any known process
---------------------------------------------------------------------------
 Particle | status  | helicity |   | E       | P_x     | P_y     | P_z      
---------------------------------------------------------------------------
         g        -1        -1          137.9       0.0       0.0     137.9
         d        -1        -1         1101.6       0.0       0.0   -1101.6
    Higgs0         1         0          301.7    -177.9     -39.3    -205.4
         b         1        -1           92.2      12.6     -73.7     -54.0
      nu_e         1        -1          165.8      81.8      50.6    -135.1
        e+         1         1           59.5      -7.9     -11.2     -57.9
    anti-b         1         1           55.8      33.7      42.7      12.5
         d         1        -1           89.6      28.7       9.4     -84.3
    anti-c         1         1           63.7     -40.0     -28.4     -40.6
         d         1        -1          365.8      76.4      37.9    -355.7
         g         1        -1           45.3      -7.5      11.9     -43.0
[1.0, 1.0, 1.0]
 
>> Event with PDGs [21, 21, 25, 5, 4, -3, -5, 1, -2] does not match any known process
---------------------------------------------------------------------------
 Particle | status  | helicity |   | E       | P_x     | P_y     | P_z      
---------------------------------------------------------------------------
         g        -1         1           85.7       0.0       0.0      85.7
         g        -1         1         1177.8       0.0       0.0   -1177.8
    Higgs0         1         0          279.0      34.2     -11.9    -246.8
         b         1        -1          291.4       1.8      34.0    -289.4
         c         1        -1           44.7     -18.5      10.4     -39.3
    anti-s         1         1          425.7     -51.7    -111.0    -407.8
    anti-b         1         1           42.6     -23.3     -34.4      -9.2
         d         1        -1           33.1      -4.2      -2.6     -32.8
    anti-u         1         1          147.0      61.6     115.5     -66.8
[1.0, 1.0, 1.0]
 
>> Event with PDGs [2, 21, 25, 5, 2, -1, -5, 3, -4, 2, 21] does not match any known process
---------------------------------------------------------------------------
 Particle | status  | helicity |   | E       | P_x     | P_y     | P_z      
---------------------------------------------------------------------------
         u        -1         1         1470.5       0.0       0.0    1470.5
         g        -1         1           58.3       0.0       0.0     -58.3
    Higgs0         1         0          346.6       3.2      31.1     321.8
         b         1        -1          367.0       0.2      41.2     364.7
         u         1        -1          152.7      73.4     -30.7     130.3
    anti-d         1         1           78.3     -19.0     -13.7      74.7
    anti-b         1         1          247.2      40.8      18.3     243.1
         s         1        -1           14.9      10.4       8.4      -6.7
    anti-c         1         1          124.2     -61.9       8.0     107.4
         u         1         1          133.9     -50.8     -37.6     118.1
         g         1         1           63.9       3.8     -24.9      58.7
[1.0, 1.0, 1.0]
 
>> Event with PDGs [21, 21, 25, 5, 14, -13, -5, 13, -14, 21] does not match any known process
---------------------------------------------------------------------------
 Particle | status  | helicity |   | E       | P_x     | P_y     | P_z      
---------------------------------------------------------------------------
         g        -1         1          307.5       0.0       0.0     307.5
         g        -1         1          526.8       0.0       0.0    -526.8
    Higgs0         1         0          302.9      59.9      86.9    -254.9
         b         1        -1           73.7      69.9     -21.5       9.5
     nu_mu         1        -1          106.6     -32.2      15.9    -100.4
       mu+         1         1           26.0      25.7       2.2      -3.7
    anti-b         1         1          109.9     -67.5     -84.5      19.5
       mu-         1        -1           21.6       5.8      13.2     -16.1
anti-nu_mu         1         1           99.5     -85.8      24.9      43.8
         g         1         1           94.1      24.3     -37.1      83.0
[1.0, 1.0, 1.0]
 
>> Event with PDGs [21, 21, 25, 5, 14, -13, -5, 1, -2, 21, 21] does not match any known process
---------------------------------------------------------------------------
 Particle | status  | helicity |   | E       | P_x     | P_y     | P_z      
---------------------------------------------------------------------------
         g        -1         1          298.1       0.0       0.0     298.1
         g        -1        -1         1359.1       0.0       0.0   -1359.1
    Higgs0         1         0          321.9      93.0      46.2    -277.9
         b         1        -1           76.5      74.6      -0.7      17.0
     nu_mu         1        -1           38.3     -18.4      20.2      26.9
       mu+         1         1          136.5     -13.9     -28.7     132.7
    anti-b         1         1          269.1     -38.6     -61.0    -259.2
         d         1        -1          399.4     -74.8      17.5    -392.0
    anti-u         1         1          312.7       2.3      52.1    -308.3
         g         1         1           72.6     -24.0     -64.2      23.8
         g         1         1           30.4      -0.2      18.6     -24.0
[1.0, 1.0, 1.0]
 
Processed 10 preselected entries from root://xrootd-cms.infn.it//store/mc/RunIISummer19UL18NanoAODv2/ttHJetToGG_M125_TuneCP5_13TeV-amcatnloFXFX-madspin-pythia8_storeWeights/NANOAODSIM/106X_upgrade2018_realistic_v15_L1v1-v1/40000/3A2BC04C-E3DA-A142-A7DB-8421AA9C8BE2.root (10 entries). Finally selected 10 entries
Done ./3A2BC04C-E3DA-A142-A7DB-8421AA9C8BE2_Skim.root
Total time 4.6 sec. to process 10 events. Rate = 2.2 Hz.
```

</p>
</details> 

Let's inspect the output closely. We produced a reweighting module with `p p > t t~ h` and this is reflected in the accepted PDG lists (see beginning of output). However, the event summaries do not correspond to what the reweighting module expects. There are two reasons for this:
1. Instead of the top quarks themselves, we have decay products of the top quarks.
2. There are events which have additional jets which come from a process line like `p p > h t t~ j j`.

Let's first focus on the first problem and to fix it we will use GenPart.

```
python scripts/run_reweighting.py path/to/output \
 root://xrootd-cms.infn.it//store/mc/RunIISummer19UL18NanoAODv2/ttHJetToGG_M125_TuneCP5_13TeV-amcatnloFXFX-madspin-pythia8_storeWeights/NANOAODSIM/106X_upgrade2018_realistic_v15_L1v1-v1/40000/3A2BC04C-E3DA-A142-A7DB-8421AA9C8BE2.root \
 path/to/rw_module -N 10 -v -m Gen
```

<details>
<summary>Click here to see the output of this command.</summary>
<p>

```
[mknight@lxplus740 NanoAODTools]$ python scripts/run_reweighting.py .  root://xrootd-cms.infn.it//store/mc/RunIISummer19UL18NanoAODv2/ttHJetToGG_M125_TuneCP5_13TeV-amcatnloFXFX-madspin-pythia8_storeWeights/NANOAODSIM/106X_upgrade2018_realistic_v15_L1v1-v1/40000/3A2BC04C-E3DA-A142-A7DB-8421AA9C8BE2.root  ../../../../EFT2Obs/rw_ttH-SMEFTsim/ -N 10 -v -m Gen
>> 1 parameters, 3 reweight points
>> LO Reweighting
>> Initialising modules...
>> Reusing working directory /eos/home-m/mknight/Standalone/tidying/EFT2Obs/rw_ttH-SMEFTsim
>> StandaloneReweight class initialized
>> Accepted PDG lists:
   - [4, -4, 25, 6, -6]
   - [21, 21, 25, 6, -6]
   - [2, -2, 25, 6, -6]
   - [3, -1, 25, 6, -6]
   - [1, -3, 25, 6, -6]
   - [1, -1, 25, 6, -6]
   - [3, -3, 25, 6, -6]
Will write selected trees to .
Pre-select 10 entries out of 10 (100.00%)
>> Event with PDGs [2, -2, 25, 6, -6, 5, 24, -5, -24, 2, -1, 3, -4, 22, 22] does not match any known process
---------------------------------------------------------------------------
 Particle | status  | helicity |   | E       | P_x     | P_y     | P_z      
---------------------------------------------------------------------------
         u        -1      None          122.2       0.0       0.0     122.2
    anti-u        -1      None         1034.5       0.0       0.0   -1034.5
    Higgs0         1      None          566.4      65.7      98.9    -539.5
         t         1      None          179.6      26.1     -63.3     -12.7
    anti-t         1      None          409.8     -91.7     -35.4    -359.2
         b         1      None           48.2     -16.6      29.9     -33.8
        W+         1      None          130.6      41.3     -91.9      22.7
    anti-b         1      None          247.8    -102.6       5.7    -225.5
        W-         1      None          161.6       9.7     -41.9    -133.0
         u         1      None           75.1      -4.4     -74.9      -3.8
    anti-d         1      None           55.5      45.7     -17.0      26.5
         s         1      None           92.2     -34.2     -26.8     -81.2
    anti-c         1      None           69.6      43.7     -15.0     -52.0
     gamma         1      None          200.1     -15.2      80.1    -182.7
     gamma         1      None          366.6      79.3      17.8    -357.5
[1.0, 1.0, 1.0]
 
>> Event with PDGs [21, 21, 25, 6, -6, 21, 5, 24, -5, -24, 2, -1, 3, -4, 22, 22] does not match any known process
---------------------------------------------------------------------------
 Particle | status  | helicity |   | E       | P_x     | P_y     | P_z      
---------------------------------------------------------------------------
         g        -1      None          422.4       0.0       0.0     422.4
         g        -1      None          570.0       0.0       0.0    -570.0
    Higgs0         1      None          268.4    -171.4    -152.6     -61.0
         t         1      None          225.2    -124.8     -41.5      63.5
    anti-t         1      None          335.4     135.0     186.9    -173.5
         g         1      None          163.7     161.9       6.6      23.3
         b         1      None          116.0     -91.3     -71.6       1.0
        W+         1      None          110.7     -35.8      28.1      61.8
    anti-b         1      None          199.1      51.7     157.7    -109.9
        W-         1      None          138.5      57.9      19.1     -93.7
         u         1      None           45.8     -20.3      41.0       0.3
    anti-d         1      None           64.2     -15.6     -13.9      60.7
         s         1      None           53.5     -11.3      30.5     -42.4
    anti-c         1      None           84.0      67.5      -6.2     -49.7
     gamma         1      None          220.6    -179.7    -127.8      -7.9
     gamma         1      None           58.7      -5.0     -30.3     -50.1
[1.0, 1.0, 1.0]
 
>> Event with PDGs [21, 21, 25, 6, -6, 5, 24, -5, -24, 4, -3, 1, -2, 22, 22] does not match any known process
---------------------------------------------------------------------------
 Particle | status  | helicity |   | E       | P_x     | P_y     | P_z      
---------------------------------------------------------------------------
         g        -1      None          332.7       0.0       0.0     332.7
         g        -1      None          351.1       0.0       0.0    -351.1
    Higgs0         1      None          179.7       9.7     -48.1    -119.4
         t         1      None          235.3     146.8      51.3     -35.7
    anti-t         1      None          268.5    -156.5      -2.6     136.7
         b         1      None          144.7     124.9      61.1     -40.3
        W+         1      None           84.5      14.6     -17.8       2.9
    anti-b         1      None           63.5     -39.9      49.4      -1.5
        W-         1      None          208.7    -128.1     -58.9     131.7
         c         1      None           50.3       6.4     -47.7      14.7
    anti-s         1      None           34.1       9.0      30.6     -12.1
         d         1      None           37.7     -27.3     -25.5      -4.7
    anti-u         1      None          141.6     -83.0     -17.2     113.4
     gamma         1      None           98.2      34.8      17.6     -90.1
     gamma         1      None           84.2     -28.4     -73.2     -30.5
[1.0, 1.0, 1.0]
 
>> Event with PDGs [21, 21, 25, 6, -6, 5, 24, -5, -24, 2, -1, -16, 15, 22, 22] does not match any known process
---------------------------------------------------------------------------
 Particle | status  | helicity |   | E       | P_x     | P_y     | P_z      
---------------------------------------------------------------------------
         g        -1      None          586.3       0.0       0.0     586.3
         g        -1      None          128.9       0.0       0.0    -128.9
    Higgs0         1      None          269.0       0.8       6.4     238.2
         t         1      None          253.7      13.7      64.0     174.6
    anti-t         1      None          191.4     -14.5     -70.5      43.3
         b         1      None           43.7     -43.4       0.7       5.6
        W+         1      None          227.5      58.4      60.0     195.1
    anti-b         1      None          103.8     -63.9     -56.9      58.8
        W-         1      None           93.1      47.9     -15.5       2.1
         u         1      None           46.2      37.7      -3.4      26.4
    anti-d         1      None          181.2      20.5      63.3     168.6
anti-nu_tau         1      None           37.5      13.0      17.3      30.6
      tau-         1      None           55.3      34.3     -32.8     -28.3
     gamma         1      None           65.1      37.1      33.0      42.1
     gamma         1      None          229.5     -34.2     -32.4     224.6
[1.0, 1.0, 1.0]
 
>> Event with PDGs [21, 21, 25, 6, -6, 5, 24, -5, -24, 16, -15, 13, -14, 22, 22] does not match any known process
---------------------------------------------------------------------------
 Particle | status  | helicity |   | E       | P_x     | P_y     | P_z      
---------------------------------------------------------------------------
         g        -1      None          302.6       0.0       0.0     302.6
         g        -1      None          468.1       0.0       0.0    -468.1
    Higgs0         1      None          137.4     -27.2     -27.4      42.1
         t         1      None          260.8      93.7     148.4      92.2
    anti-t         1      None          372.8     -66.1    -121.1    -300.2
         b         1      None           60.7      21.7     -12.9      55.2
        W+         1      None          201.7      66.4     168.4      35.9
    anti-b         1      None          220.2     -76.0     -30.7    -204.4
        W-         1      None          148.9       3.6     -83.4     -92.7
    nu_tau         1      None          137.9      80.0     106.3      36.4
      tau+         1      None           59.9     -15.0      58.0      -0.5
       mu-         1      None           31.5      19.8       9.5     -22.5
anti-nu_mu         1      None          117.3     -17.0     -91.9     -70.8
     gamma         1      None           64.4      40.1      -3.4      50.3
     gamma         1      None           72.9     -69.9     -19.1      -7.4
[1.0, 1.0, 1.0]
 
>> Event with PDGs [21, 1, 25, 6, -6, 1, 21, 5, 24, -5, -24, 12, -11, 1, -4, 22, 22] does not match any known process
---------------------------------------------------------------------------
 Particle | status  | helicity |   | E       | P_x     | P_y     | P_z      
---------------------------------------------------------------------------
         g        -1      None          137.9       0.0       0.0     137.9
         d        -1      None         1101.5       0.0       0.0   -1101.5
    Higgs0         1      None          301.4    -177.6     -39.7    -205.2
         t         1      None          317.4      86.4     -34.3    -246.9
    anti-t         1      None          208.8      22.4      23.7    -112.2
         d         1      None          364.7      76.4      37.9    -354.6
         g         1      None           45.2      -7.5      11.9     -43.0
         b         1      None           89.6      11.5     -72.8     -50.9
        W+         1      None          217.6      70.9      41.1    -184.6
    anti-b         1      None           55.8      32.7      43.9      10.5
        W-         1      None          157.4     -13.6     -15.6    -130.2
      nu_e         1      None          160.2      79.6      51.9    -129.0
        e+         1      None           57.6      -8.7     -10.8     -55.9
         d         1      None           92.0      27.4      11.5     -87.1
    anti-c         1      None           64.9     -41.0     -26.8     -42.5
     gamma         1      None           23.8     -10.2     -16.7      13.5
     gamma         1      None          286.3    -172.4     -19.1    -227.7
[1.0, 1.0, 1.0]
 
>> Event with PDGs [21, 21, 25, 6, -6, 5, 24, -5, -24, 4, -3, 1, -2, 22, 22] does not match any known process
---------------------------------------------------------------------------
 Particle | status  | helicity |   | E       | P_x     | P_y     | P_z      
---------------------------------------------------------------------------
         g        -1      None           85.7       0.0       0.0      85.7
         g        -1      None         1177.8       0.0       0.0   -1177.8
    Higgs0         1      None          279.1      34.2     -11.9    -246.9
         t         1      None          763.4     -68.3     -66.8    -738.0
    anti-t         1      None          222.8      34.1      78.4    -108.9
         b         1      None          292.2      -2.8      33.3    -290.3
        W+         1      None          474.0     -77.7    -101.1    -449.5
    anti-b         1      None           45.3     -21.7     -39.1      -7.0
        W-         1      None          165.7      62.9      94.2     -90.3
         c         1      None           43.6     -18.7      11.0     -37.8
    anti-s         1      None          410.7     -53.7    -104.2    -393.7
         d         1      None           31.6      -3.5      -6.6     -30.7
    anti-u         1      None          130.9      64.6      98.1     -57.6
     gamma         1      None          201.3       4.0      37.8    -197.7
     gamma         1      None           82.1      27.9     -55.1     -54.1
[1.0, 1.0, 1.0]
 
>> Event with PDGs [2, 21, 25, 6, -6, 2, 21, 5, 24, -5, -24, 2, -1, 3, -4, 22, 22] does not match any known process
---------------------------------------------------------------------------
 Particle | status  | helicity |   | E       | P_x     | P_y     | P_z      
---------------------------------------------------------------------------
         u        -1      None         1470.5       0.0       0.0    1470.5
         g        -1      None           58.3       0.0       0.0     -58.3
    Higgs0         1      None          345.4       3.2      31.1     320.5
         t         1      None          597.3      54.5      -3.3     569.1
    anti-t         1      None          387.4     -10.8      34.7     344.9
         u         1      None          134.0     -51.0     -37.5     118.1
         g         1      None           64.0       3.8     -25.0      58.8
         b         1      None          360.3       2.7      42.0     357.8
        W+         1      None          228.1      55.9     -43.8     201.4
    anti-b         1      None          241.1      46.2      17.8     236.0
        W-         1      None          135.2     -48.4      16.1      96.9
         u         1      None          149.7      73.2     -29.0     127.3
    anti-d         1      None           76.8     -19.0     -12.9      73.3
         s         1      None           15.4      10.8       8.4      -7.1
    anti-c         1      None          119.7     -58.3       7.9     104.2
     gamma         1      None          209.1     -47.1      49.8     197.6
     gamma         1      None          130.2      55.8     -18.5     116.2
[1.0, 1.0, 1.0]
 
>> Event with PDGs [21, 21, 25, 6, -6, 21, 5, 24, -5, -24, 14, -13, 13, -14, 22, 22] does not match any known process
---------------------------------------------------------------------------
 Particle | status  | helicity |   | E       | P_x     | P_y     | P_z      
---------------------------------------------------------------------------
         g        -1      None          307.5       0.0       0.0     307.5
         g        -1      None          526.8       0.0       0.0    -526.8
    Higgs0         1      None          303.2      59.9      86.8    -255.3
         t         1      None          206.4      63.4      -3.4     -94.9
    anti-t         1      None          230.9    -147.3     -46.5      47.2
         g         1      None           94.3      24.3     -37.2      83.2
         b         1      None           73.9      70.0     -21.6       9.6
        W+         1      None          132.3      -6.3      17.9    -103.7
    anti-b         1      None          110.3     -68.3     -84.6      18.6
        W-         1      None          121.2     -80.6      37.8      26.8
     nu_mu         1      None          102.7     -30.7      15.0     -96.8
       mu+         1      None           26.3      26.0       2.0      -2.8
       mu-         1      None           21.6       5.7      13.1     -16.2
anti-nu_mu         1      None           99.5     -86.4      24.3      43.0
     gamma         1      None          163.1      90.7      63.6    -119.7
     gamma         1      None          138.6     -29.0      23.1    -133.6
[1.0, 1.0, 1.0]
 
>> Event with PDGs [21, 21, 25, 6, -6, 21, 21, 5, 24, -5, -24, 14, -13, 1, -2, 22, 22] does not match any known process
---------------------------------------------------------------------------
 Particle | status  | helicity |   | E       | P_x     | P_y     | P_z      
---------------------------------------------------------------------------
         g        -1      None          298.1       0.0       0.0     298.1
         g        -1      None         1359.1       0.0       0.0   -1359.1
    Higgs0         1      None          321.7      92.9      46.2    -277.7
         t         1      None          251.0      42.4      -9.2     176.1
    anti-t         1      None          983.8    -111.2       8.8    -962.1
         g         1      None           72.5     -24.1     -64.1      23.7
         g         1      None           30.3      -0.2      18.6     -24.0
         b         1      None           76.9      75.0      -2.2      16.8
        W+         1      None          173.7     -31.3     -12.1     158.4
    anti-b         1      None          263.4     -35.6     -59.7    -254.1
        W-         1      None          697.1     -64.7      72.9    -685.5
     nu_mu         1      None           34.8     -16.9      19.7      23.1
       mu+         1      None          123.8      -8.5     -30.5     119.7
         d         1      None          388.4     -70.2      19.2    -381.6
    anti-u         1      None          307.5       5.9      53.4    -302.8
     gamma         1      None          206.1      35.2      83.6    -185.0
     gamma         1      None          117.5      60.3     -37.0     -93.8
[1.0, 1.0, 1.0]
 
Processed 10 preselected entries from root://xrootd-cms.infn.it//store/mc/RunIISummer19UL18NanoAODv2/ttHJetToGG_M125_TuneCP5_13TeV-amcatnloFXFX-madspin-pythia8_storeWeights/NANOAODSIM/106X_upgrade2018_realistic_v15_L1v1-v1/40000/3A2BC04C-E3DA-A142-A7DB-8421AA9C8BE2.root (10 entries). Finally selected 10 entries
Done ./3A2BC04C-E3DA-A142-A7DB-8421AA9C8BE2_Skim.root
Total time 4.2 sec. to process 10 events. Rate = 2.4 Hz.
```

</p>
</details> 

In addition to all the particles we saw before, we know see the top quarks and the photons from the Higgs decay. However, the reweighting module still does not know what to do because it expects *only* `p p > h t t~`. So we need to write our own reweighting method to select just only `p p > h t t~`. To do this, start by looking at [reweighter.py](../python/postprocessing/modules/reweighting/reweighter.py). 

We will need to define a new class that will describe how to select `p p > h t t~`. To begin with we can look at the LHEReweighter and GenReweighter classes. These correspond to the LHE and Gen methods shown already. For this example we will make a new class called ttHReweighter which inherits the GenReweighter class. The simplest way to select the relevant particles is to rewrite the filterPart function and require that on top of the previous requirements, that the particles are also either incoming partons or are a Higgs, top, or anti-top. A class that does this would look like:

```py
class ttHReweighter(GenReweighter):
  def filterPart(self, part, event, index):
    if GenReweighter.filterPart(self, part, event, index):
      if self.isIncomingParton(part, event, index):
        return True
      elif part.pdgId in [25, 6, -6]:
        return True
      else:
        return False
```

We'll see later that this approach is actually problematic but let's see what happens anyway. We can use our new method by specifying `-m ttH`:
```
python scripts/run_reweighting.py path/to/output \
 root://xrootd-cms.infn.it//store/mc/RunIISummer19UL18NanoAODv2/ttHJetToGG_M125_TuneCP5_13TeV-amcatnloFXFX-madspin-pythia8_storeWeights/NANOAODSIM/106X_upgrade2018_realistic_v15_L1v1-v1/40000/3A2BC04C-E3DA-A142-A7DB-8421AA9C8BE2.root \
 path/to/rw_module -N 10 -v -m ttH
```

<details>
<summary>Click here to see the output of this command.</summary>
<p>

```
[mknight@lxplus737 NanoAODTools]$ python scripts/run_reweighting.py .  root://xrootd-cms.infn.it//store/mc/RunIISummer19UL18NanoAODv2/ttHJetToGG_M125_TuneCP5_13TeV-amcatnloFXFX-madspin-pythia8_storeWeights/NANOAODSIM/106X_upgrade2018_realistic_v15_L1v1-v1/40000/3A2BC04C-E3DA-A142-A7DB-8421AA9C8BE2.root  ../../../../EFT2Obs/rw_ttH-SMEFTsim/ -N 10 -v -m ttH
>> 1 parameters, 3 reweight points
>> LO Reweighting
>> Initialising modules...
>> Reusing working directory /eos/home-m/mknight/Standalone/tidying/EFT2Obs/rw_ttH-SMEFTsim
>> StandaloneReweight class initialized
>> Accepted PDG lists:
   - [4, -4, 25, 6, -6]
   - [21, 21, 25, 6, -6]
   - [2, -2, 25, 6, -6]
   - [3, -1, 25, 6, -6]
   - [1, -3, 25, 6, -6]
   - [1, -1, 25, 6, -6]
   - [3, -3, 25, 6, -6]
Will write selected trees to .
Pre-select 10 entries out of 10 (100.00%)
---------------------------------------------------------------------------
 Particle | status  | helicity |   | E       | P_x     | P_y     | P_z      
---------------------------------------------------------------------------
         u        -1      None          122.2       0.0       0.0     122.2
    anti-u        -1      None         1034.5       0.0       0.0   -1034.5
    Higgs0         1      None          566.4      65.7      98.9    -539.5
         t         1      None          179.6      26.1     -63.3     -12.7
    anti-t         1      None          409.8     -91.7     -35.4    -359.2
[1.0, 1.0026648395928082, 1.005333395740219]
 
---------------------------------------------------------------------------
 Particle | status  | helicity |   | E       | P_x     | P_y     | P_z      
---------------------------------------------------------------------------
         g        -1      None          422.4       0.0       0.0     422.4
         g        -1      None          570.0       0.0       0.0    -570.0
    Higgs0         1      None          268.4    -171.4    -152.6     -61.0
         t         1      None          225.2    -124.8     -41.5      63.5
    anti-t         1      None          335.4     135.0     186.9    -173.5
[1.0, 1.00184134039658, 1.003704841317463]
 
---------------------------------------------------------------------------
 Particle | status  | helicity |   | E       | P_x     | P_y     | P_z      
---------------------------------------------------------------------------
         g        -1      None          332.7       0.0       0.0     332.7
         g        -1      None          351.1       0.0       0.0    -351.1
    Higgs0         1      None          179.7       9.7     -48.1    -119.4
         t         1      None          235.3     146.8      51.3     -35.7
    anti-t         1      None          268.5    -156.5      -2.6     136.7
[1.0, 1.0022504430528785, 1.0045119523475206]
 
---------------------------------------------------------------------------
 Particle | status  | helicity |   | E       | P_x     | P_y     | P_z      
---------------------------------------------------------------------------
         g        -1      None          586.3       0.0       0.0     586.3
         g        -1      None          128.9       0.0       0.0    -128.9
    Higgs0         1      None          269.0       0.8       6.4     238.2
         t         1      None          253.7      13.7      64.0     174.6
    anti-t         1      None          191.4     -14.5     -70.5      43.3
[1.0, 1.0023113352508244, 1.0046277401731876]
 
---------------------------------------------------------------------------
 Particle | status  | helicity |   | E       | P_x     | P_y     | P_z      
---------------------------------------------------------------------------
         g        -1      None          302.6       0.0       0.0     302.6
         g        -1      None          468.1       0.0       0.0    -468.1
    Higgs0         1      None          137.4     -27.2     -27.4      42.1
         t         1      None          260.8      93.7     148.4      92.2
    anti-t         1      None          372.8     -66.1    -121.1    -300.2
[1.0, 1.0023334202681022, 1.0046772172716278]
 
>> Event with PDGs [21, 1, 25, 6, -6] does not match any known process
---------------------------------------------------------------------------
 Particle | status  | helicity |   | E       | P_x     | P_y     | P_z      
---------------------------------------------------------------------------
         g        -1      None          137.9       0.0       0.0     137.9
         d        -1      None         1101.5       0.0       0.0   -1101.5
    Higgs0         1      None          301.4    -177.6     -39.7    -205.2
         t         1      None          317.4      86.4     -34.3    -246.9
    anti-t         1      None          208.8      22.4      23.7    -112.2
[1.0, 1.0, 1.0]
 
---------------------------------------------------------------------------
 Particle | status  | helicity |   | E       | P_x     | P_y     | P_z      
---------------------------------------------------------------------------
         g        -1      None           85.7       0.0       0.0      85.7
         g        -1      None         1177.8       0.0       0.0   -1177.8
    Higgs0         1      None          279.1      34.2     -11.9    -246.9
         t         1      None          763.4     -68.3     -66.8    -738.0
    anti-t         1      None          222.8      34.1      78.4    -108.9
[1.0, 1.0023810061591285, 1.0047699654879791]
 
>> Event with PDGs [2, 21, 25, 6, -6] does not match any known process
---------------------------------------------------------------------------
 Particle | status  | helicity |   | E       | P_x     | P_y     | P_z      
---------------------------------------------------------------------------
         u        -1      None         1470.5       0.0       0.0    1470.5
         g        -1      None           58.3       0.0       0.0     -58.3
    Higgs0         1      None          345.4       3.2      31.1     320.5
         t         1      None          597.3      54.5      -3.3     569.1
    anti-t         1      None          387.4     -10.8      34.7     344.9
[1.0, 1.0, 1.0]
 
---------------------------------------------------------------------------
 Particle | status  | helicity |   | E       | P_x     | P_y     | P_z      
---------------------------------------------------------------------------
         g        -1      None          307.5       0.0       0.0     307.5
         g        -1      None          526.8       0.0       0.0    -526.8
    Higgs0         1      None          303.2      59.9      86.8    -255.3
         t         1      None          206.4      63.4      -3.4     -94.9
    anti-t         1      None          230.9    -147.3     -46.5      47.2
[1.0, 1.003573231364754, 1.0071705186374615]
 
---------------------------------------------------------------------------
 Particle | status  | helicity |   | E       | P_x     | P_y     | P_z      
---------------------------------------------------------------------------
         g        -1      None          298.1       0.0       0.0     298.1
         g        -1      None         1359.1       0.0       0.0   -1359.1
    Higgs0         1      None          321.7      92.9      46.2    -277.7
         t         1      None          251.0      42.4      -9.2     176.1
    anti-t         1      None          983.8    -111.2       8.8    -962.1
[1.0, 0.9983691769300148, 0.9967775710442139]
 
Processed 10 preselected entries from root://xrootd-cms.infn.it//store/mc/RunIISummer19UL18NanoAODv2/ttHJetToGG_M125_TuneCP5_13TeV-amcatnloFXFX-madspin-pythia8_storeWeights/NANOAODSIM/106X_upgrade2018_realistic_v15_L1v1-v1/40000/3A2BC04C-E3DA-A142-A7DB-8421AA9C8BE2.root (10 entries). Finally selected 10 entries
Done ./3A2BC04C-E3DA-A142-A7DB-8421AA9C8BE2_Skim.root
Total time 4.9 sec. to process 10 events. Rate = 2.1 Hz.
```

</p>
</details> 

We can now see that we have only `h t t~` which was our intention. However, the additional jets which we saw previously have also been removed and we need those jets to do the reweighting correctly. So, we need a way of selecting `h t t~` and the jets. By inspecting the NanoAOD file (with uproot or your favourite root reading method) we can notice that the outgoing particles from the hard interaction have their mother as the first incoming parton (index=0). We can use this fact to select the correct particles:

```py
class ttHReweighter(GenReweighter):
  def filterPart(self, part, event, index):
    if GenReweighter.filterPart(self, part, event, index):
      if self.isIncomingParton(part, event, index):
        return True
      #elif part.pdgId in [25, 6, -6]:
      #  return True
      elif part.genPartIdxMother==0:
        return True
      else:
        return False
```

and rerun the reweighting. 

<details>
<summary>Click here to see the output of this command.</summary>
<p>

```
[mknight@lxplus737 NanoAODTools]$ python scripts/run_reweighting.py .  root://xrootd-cms.infn.it//store/mc/RunIISummer19UL18NanoAODv2/ttHJetToGG_M125_TuneCP5_13TeV-amcatnloFXFX-madspin-pythia8_storeWeights/NANOAODSIM/106X_upgrade2018_realistic_v15_L1v1-v1/40000/3A2BC04C-E3DA-A142-A7DB-8421AA9C8BE2.root  ../../../../EFT2Obs/rw_ttH-SMEFTsim/ -N 10 -v -m ttH
>> 1 parameters, 3 reweight points
>> LO Reweighting
>> Initialising modules...
>> Reusing working directory /eos/home-m/mknight/Standalone/tidying/EFT2Obs/rw_ttH-SMEFTsim
>> StandaloneReweight class initialized
>> Accepted PDG lists:
   - [4, -4, 25, 6, -6]
   - [21, 21, 25, 6, -6]
   - [2, -2, 25, 6, -6]
   - [3, -1, 25, 6, -6]
   - [1, -3, 25, 6, -6]
   - [1, -1, 25, 6, -6]
   - [3, -3, 25, 6, -6]
Will write selected trees to .
Pre-select 10 entries out of 10 (100.00%)
---------------------------------------------------------------------------
 Particle | status  | helicity |   | E       | P_x     | P_y     | P_z      
---------------------------------------------------------------------------
         u        -1      None          122.2       0.0       0.0     122.2
    anti-u        -1      None         1034.5       0.0       0.0   -1034.5
    Higgs0         1      None          566.4      65.7      98.9    -539.5
         t         1      None          179.6      26.1     -63.3     -12.7
    anti-t         1      None          409.8     -91.7     -35.4    -359.2
[1.0, 1.0026648395928082, 1.005333395740219]
 
>> Event with PDGs [21, 21, 25, 6, -6, 21] does not match any known process
---------------------------------------------------------------------------
 Particle | status  | helicity |   | E       | P_x     | P_y     | P_z      
---------------------------------------------------------------------------
         g        -1      None          422.4       0.0       0.0     422.4
         g        -1      None          570.0       0.0       0.0    -570.0
    Higgs0         1      None          268.4    -171.4    -152.6     -61.0
         t         1      None          225.2    -124.8     -41.5      63.5
    anti-t         1      None          335.4     135.0     186.9    -173.5
         g         1      None          163.7     161.9       6.6      23.3
[1.0, 1.0, 1.0]
 
---------------------------------------------------------------------------
 Particle | status  | helicity |   | E       | P_x     | P_y     | P_z      
---------------------------------------------------------------------------
         g        -1      None          332.7       0.0       0.0     332.7
         g        -1      None          351.1       0.0       0.0    -351.1
    Higgs0         1      None          179.7       9.7     -48.1    -119.4
         t         1      None          235.3     146.8      51.3     -35.7
    anti-t         1      None          268.5    -156.5      -2.6     136.7
[1.0, 1.0022504430528785, 1.0045119523475206]
 
---------------------------------------------------------------------------
 Particle | status  | helicity |   | E       | P_x     | P_y     | P_z      
---------------------------------------------------------------------------
         g        -1      None          586.3       0.0       0.0     586.3
         g        -1      None          128.9       0.0       0.0    -128.9
    Higgs0         1      None          269.0       0.8       6.4     238.2
         t         1      None          253.7      13.7      64.0     174.6
    anti-t         1      None          191.4     -14.5     -70.5      43.3
[1.0, 1.0023113352508244, 1.0046277401731876]
 
---------------------------------------------------------------------------
 Particle | status  | helicity |   | E       | P_x     | P_y     | P_z      
---------------------------------------------------------------------------
         g        -1      None          302.6       0.0       0.0     302.6
         g        -1      None          468.1       0.0       0.0    -468.1
    Higgs0         1      None          137.4     -27.2     -27.4      42.1
         t         1      None          260.8      93.7     148.4      92.2
    anti-t         1      None          372.8     -66.1    -121.1    -300.2
[1.0, 1.0023334202681022, 1.0046772172716278]
 
>> Event with PDGs [21, 1, 25, 6, -6, 1, 21] does not match any known process
---------------------------------------------------------------------------
 Particle | status  | helicity |   | E       | P_x     | P_y     | P_z      
---------------------------------------------------------------------------
         g        -1      None          137.9       0.0       0.0     137.9
         d        -1      None         1101.5       0.0       0.0   -1101.5
    Higgs0         1      None          301.4    -177.6     -39.7    -205.2
         t         1      None          317.4      86.4     -34.3    -246.9
    anti-t         1      None          208.8      22.4      23.7    -112.2
         d         1      None          364.7      76.4      37.9    -354.6
         g         1      None           45.2      -7.5      11.9     -43.0
[1.0, 1.0, 1.0]
 
---------------------------------------------------------------------------
 Particle | status  | helicity |   | E       | P_x     | P_y     | P_z      
---------------------------------------------------------------------------
         g        -1      None           85.7       0.0       0.0      85.7
         g        -1      None         1177.8       0.0       0.0   -1177.8
    Higgs0         1      None          279.1      34.2     -11.9    -246.9
         t         1      None          763.4     -68.3     -66.8    -738.0
    anti-t         1      None          222.8      34.1      78.4    -108.9
[1.0, 1.0023810061591285, 1.0047699654879791]
 
>> Event with PDGs [2, 21, 25, 6, -6, 2, 21] does not match any known process
---------------------------------------------------------------------------
 Particle | status  | helicity |   | E       | P_x     | P_y     | P_z      
---------------------------------------------------------------------------
         u        -1      None         1470.5       0.0       0.0    1470.5
         g        -1      None           58.3       0.0       0.0     -58.3
    Higgs0         1      None          345.4       3.2      31.1     320.5
         t         1      None          597.3      54.5      -3.3     569.1
    anti-t         1      None          387.4     -10.8      34.7     344.9
         u         1      None          134.0     -51.0     -37.5     118.1
         g         1      None           64.0       3.8     -25.0      58.8
[1.0, 1.0, 1.0]
 
>> Event with PDGs [21, 21, 25, 6, -6, 21] does not match any known process
---------------------------------------------------------------------------
 Particle | status  | helicity |   | E       | P_x     | P_y     | P_z      
---------------------------------------------------------------------------
         g        -1      None          307.5       0.0       0.0     307.5
         g        -1      None          526.8       0.0       0.0    -526.8
    Higgs0         1      None          303.2      59.9      86.8    -255.3
         t         1      None          206.4      63.4      -3.4     -94.9
    anti-t         1      None          230.9    -147.3     -46.5      47.2
         g         1      None           94.3      24.3     -37.2      83.2
[1.0, 1.0, 1.0]
 
>> Event with PDGs [21, 21, 25, 6, -6, 21, 21] does not match any known process
---------------------------------------------------------------------------
 Particle | status  | helicity |   | E       | P_x     | P_y     | P_z      
---------------------------------------------------------------------------
         g        -1      None          298.1       0.0       0.0     298.1
         g        -1      None         1359.1       0.0       0.0   -1359.1
    Higgs0         1      None          321.7      92.9      46.2    -277.7
         t         1      None          251.0      42.4      -9.2     176.1
    anti-t         1      None          983.8    -111.2       8.8    -962.1
         g         1      None           72.5     -24.1     -64.1      23.7
         g         1      None           30.3      -0.2      18.6     -24.0
[1.0, 1.0, 1.0]
 
Processed 10 preselected entries from root://xrootd-cms.infn.it//store/mc/RunIISummer19UL18NanoAODv2/ttHJetToGG_M125_TuneCP5_13TeV-amcatnloFXFX-madspin-pythia8_storeWeights/NANOAODSIM/106X_upgrade2018_realistic_v15_L1v1-v1/40000/3A2BC04C-E3DA-A142-A7DB-8421AA9C8BE2.root (10 entries). Finally selected 10 entries
Done ./3A2BC04C-E3DA-A142-A7DB-8421AA9C8BE2_Skim.root
Total time 5.6 sec. to process 10 events. Rate = 1.8 Hz.
```

</p>
</details> 

Now all of the relevant particles are included in the event summary. If we wanted to reweight all of the events we would have to go back and change our process lines to:
```
generate p p > h t t~
add process p p > h t t~ j
add process p p > h t t~ j j
```
We won't do that here because producing that reweighting module will take a long time due to the much larger number of diagrams.

As you can see, using GenPart and having to write your own Reweighter class can lead to mistakes if you're not careful. For that reason, it is recommended that you [validate](validation.md) your method.