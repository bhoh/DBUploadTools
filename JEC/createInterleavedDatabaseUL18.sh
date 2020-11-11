
#python createInterleavedDatabaseUL18.py --era Summer19UL18_V5_DATA  --importDB Summer19UL18_RunA_V5_DATA.db Summer19UL18_RunB_V5_DATA.db Summer19UL18_RunC_V5_DATA.db Summer19UL18_RunD_V5_DATA.db


## combine history of tags alt
for jet_type in AK4PF AK4PFchs AK4PFPuppi AK8PF AK8PFchs AK8PFPuppi
do
        conddb --yes copy --destdb offline_data_jec_alt.db  --to 315251 JetCorrectorParametersCollection_Sum16V11_and_UL17V5_and_Aut18V19_DATA_${jet_type} JetCorrectorParametersCollection_Run2_Combined_UL_2017_2018_DATA_${jet_type}
        conddb --yes copy --destdb offline_data_jec_alt.db --from 315252 --to 327564 JetCorrectorParametersCollection_Summer19UL18_V5_DATA_${jet_type} JetCorrectorParametersCollection_Run2_Combined_UL_2017_2018_DATA_${jet_type}
        conddb --yes copy --destdb offline_data_jec_alt.db  --from 327565 JetCorrectorParametersCollection_Sum16V11_and_UL17V5_and_Aut18V19_DATA_${jet_type} JetCorrectorParametersCollection_Run2_Combined_UL_2017_2018_DATA_${jet_type}
done




## combine history of tags
#for jet_type in AK4PF AK4PFchs AK4PFPuppi AK8PF AK8PFchs AK8PFPuppi
#do
#  conddb --yes copy --destdb offline_data_jec.db  --to 307082 JetCorrectorParametersCollection_Sum16V11_and_UL17V5_and_Aut18V19_DATA_${jet_type} JetCorrectorParametersCollection_Run2_Combined_UL_2017_2018_DATA_${jet_type} 
#  conddb --yes copy --destdb offline_data_jec.db --from 307083 JetCorrectorParametersCollection_Summer19UL18_V5_DATA_${jet_type} JetCorrectorParametersCollection_Run2_Combined_UL_2017_2018_DATA_${jet_type}
#done

#for sf_type in SF PtResolution PhiResolution EtaResolution
#do
#  for jet_type in AK4PFchs AK4PFPuppi AK8PFchs AK8PFPuppi
#  do
#      conddb --yes copy --destdb offline_data_jec.db  --to 307082 JR_dataRun2_RunABCD_25nsV1b_V3b_V7b_106X_DATA_${sf_type}_${jet_type} JR_dataRun2_Combined_UL_2017_2018_${sf_type}_${jet_type}
#      conddb --yes copy --destdb offline_data_jec.db --from 307083 JR_Summer19UL18_JRV2_DATA_${sf_type}_${jet_type} JR_dataRun2_Combined_UL_2017_2018_${sf_type}_${jet_type}
#  done
#done

