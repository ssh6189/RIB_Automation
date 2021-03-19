import cv2
import numpy as np
import os
import math
import pickle

'''
0. 작성자 : 함종수

1. input 
 (1-1) 

2. output 
 (2-1) 

3. algorithm : 

'''
def stirrub_calculator():

	#with open('./result_gujo/ham_gujo_result.p', 'rb') as f: ##### need to fix input #####
	    
	with open('C:/Users/cai-kvm-8/t-in/result_gujo/ham_gujo_result.p', 'rb') as f: ##### need to fix input #####
	    gujo_list = pickle.load(f) # 단 한줄씩 읽어옴

	with open('C:/Users/cai-kvm-8/t-in/result_bujae/ham_bujae_result.p', 'rb') as f: ##### need to fix input #####
	    bujae_list = pickle.load(f) # 단 한줄씩 읽어옴

	#with open('./result_bujae/ham_bujae_result.p', 'rb') as f: ##### need to fix input #####


	########## bujae_clearing ##########

	cleared_dict_list = []

	for dl in bujae_list:
	        
	    dict_temp = {}
	    dict_temp['정보'] = []
	    info_dict = {}
	    
	    for cd in cleared_dict_list:

	        if cd['부호'] == dl['부호']:
	            for info in dl:
	                if info != '부호':
	                    info_dict[info] = dl[info]

	            cd['정보'].append(info_dict)
	                                
	    if info_dict == {}:
	        dict_temp['부호'] = dl['부호']        

	        for info in dl:
	            if info != '부호':
	                info_dict[info] = dl[info]

	        dict_temp['정보'].append(info_dict)

	        cleared_dict_list.append(dict_temp)





	########## calculator ##########

	# temp_scaling_result = gujo_list.copy()

	for sr in gujo_list:
	    	    
	    for cd in cleared_dict_list:
	        
	        
	        symbol_sizes = []

	        
	        if sr[0] == cd['부호']:
	            
	            
	            if len(cd['정보']) == 1:
	                
	                stirrup_gap = 0
	                stirrup_number = 0
	                
	                stirrup_gap = int(cd['정보'][0]['늑근'][ cd['정보'][0]['늑근'].index('@')+1: ])
	                                
	                stirrup_number = math.ceil(sr[1] / stirrup_gap)
	                symbol_sizes.append({'stirrup_number': stirrup_number, 'stirrup_size': cd['정보'][0]['크기']})
	                sr.append(symbol_sizes)
	        
	        
	            elif len(cd['정보']) == 2:
	                
	                for part in cd['정보']:                
	#                     for where in part['단면']:

	                    stirrup_gap = 0
	                    stirrup_number = 0

	                    if '중앙부' in part['단면']:
	#                     if '중앙부' in where:
	                        stirrup_gap = int(part['늑근'][ part['늑근'].index('@')+1: ])
	                        stirrup_number = math.ceil(sr[1]/2 / stirrup_gap)
	                        symbol_sizes.append({'stirrup_number': stirrup_number, 'stirrup_size': part['크기']})
	                    else:
	                        stirrup_gap = int(part['늑근'][ part['늑근'].index('@')+1: ])
	                        stirrup_number = math.ceil(sr[1]/2 / stirrup_gap)
	                        symbol_sizes.append({'stirrup_number': stirrup_number, 'stirrup_size': part['크기']})
	                
	                sr.append(symbol_sizes)

	                            
	            else:
	            
	                for part in cd['정보']:                
	#                     for where in part['단면']:
	                        
	                    stirrup_gap = 0
	                    stirrup_number = 0

	                    if '중앙부' in part['단면']:
	#                     if '중앙부' in where:
	                        stirrup_gap = int(part['늑근'][ part['늑근'].index('@')+1: ])
	                        stirrup_number = math.ceil(sr[1]/2 / stirrup_gap)
	                        symbol_sizes.append({'stirrup_number': stirrup_number, 'stirrup_size': part['크기']})
	                    else:
	                        stirrup_gap = int(part['늑근'][ part['늑근'].index('@')+1: ])
	                        stirrup_number = math.ceil(sr[1]/4 / stirrup_gap)
	                        symbol_sizes.append({'stirrup_number': stirrup_number, 'stirrup_size': part['크기']})
	                
	                sr.append(symbol_sizes)

	return sr, gujo_list

	'''                
	for sr in gujo_list:
	    if len(sr) == 3:
	        for sizes in sr[2]:
	            print(sr[0], sr[1], sizes)
    '''

	# print(temp_scaling_result)       