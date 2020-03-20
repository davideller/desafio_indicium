import pandas as pd
import argparse
import re
import os.path

def main():

	#ARGUMENTS
	parser = argparse.ArgumentParser()

	parser.add_argument('-s', '--sector_data_filepath', required = True, help = 'filepath to sector data')
	parser.add_argument('-c', '--contacts_data_filepath', required = True, help = 'filepath to contacts data')
	parser.add_argument('-d', '--deals_data_filepath', required = True, help = 'filepath to deals data')
	parser.add_argument('-cp', '--companies_data_filepath', required = True, help = 'filepath to companies data')
	parser.add_argument('-o', '--output_filepath', required = True, help = 'filepath desired to save output')

	args = parser.parse_args()

	sector_data_filepath = args.sector_data_filepath
	contacts_data_filepath = args.contacts_data_filepath
	deals_data_filepath = args.deals_data_filepath
	companies_data_filepath = args.companies_data_filepath
	output_filepath = args.output_filepath

	#CHECK IF .CSV EXISTS
	inputs = [sector_data_filepath, contacts_data_filepath, deals_data_filepath, companies_data_filepath]
	for input in inputs:
		check_file = os.path.isfile(input)
		if not check_file:
			print(input, 'is not valid. Please pass a valid argument')
			return


	#LOAD DATA
	sectors_data = pd.read_csv(sector_data_filepath, sep='\t')
	contacts_data = pd.read_csv(contacts_data_filepath, sep='\t')
	companies_data = pd.read_csv(companies_data_filepath, sep='\t')


	#DROP USELESS COLUMNS
	companies_data.drop(columns = ['companiesName', 'companiesDateCreated', 'createdBy', 'companiesPhones', 'companiesEmails', \
									'usersResponsible'], inplace = True)
	contacts_data.drop(columns = ['contactsDateCreated', 'contactsCreatedBy', 'contactsEmails', 'contactsPhones', 'contactsEmployers', \
									'employersId', 'contactsHomeAdress', 'contactsLatLong', 'contactsRelatedToLead', 'contactsResponsible'], \
										inplace = True)

	#RENAME COLUMNS
	contacts_data.rename(columns = {' contactsId' :'contactsId' }, inplace = True)
	companies_data.rename(columns = {'employeesId':'contactsId'}, inplace = True)

	#LOOKS FOR NON ALPHANUMERIC CHARACTERS
	r1 = re.compile(r'[^\x00-\xFF]')  

	dropped_lines = 0
	dfs = [companies_data, sectors_data, contacts_data]

	for df in dfs:
	    for column in df.columns: 
	        for i in range(df.shape[0] - 1):
	        	if r1.findall(str(df[column][i])) != []:
		            df.drop(i, inplace = True)
		            df.reset_index(inplace = True)
		            dropped_lines = dropped_lines + 1

	#CREATES NEW DATAFRAME
	deals_data = pd.DataFrame() 


	#LOAD AND PROCESS DATA IN CHUNKS
	chunk_size = 20
	for chunk in pd.read_csv(deals_data_filepath, sep='\t', chunksize = chunk_size):

	    #Optmize dataframe size
	    chunk['dealsId'] = chunk['dealsId'].astype('int32')
	    chunk['dealsPrice'] = chunk['dealsPrice'].astype('int32')
	    chunk['contactsId'] = chunk['contactsId'].astype('int32')
	    chunk['companiesId'] = chunk['companiesId'].astype('int32')

	    
	    #Transform data to datetime
	    chunk['dealsDateCreated'] = pd.to_datetime(chunk['dealsDateCreated'])
	    chunk['month'] = chunk['dealsDateCreated'].dt.month
	    
	    #Merge data
	    chunk = chunk.merge(contacts_data[['contactsName', 'contactsId']], on='contactsId')
	    chunk = chunk.merge(companies_data[['contactsId', 'sectorKey']], on='contactsId')
	    chunk = chunk.merge(sectors_data, on='sectorKey')

	    for column in chunk.columns:
	    	for i in range(chunk.shape[0] - 1):
		        if r1.findall(chunk['contactsName'][i]) != []:
		            chunk.drop(i, inplace = True)
		            chunk.reset_index(inplace = True)
		            dropped_lines = dropped_lines + 1
		            

	    deals_data = pd.concat([chunk, deals_data])

	    #First Output
	    deals_per_month_data = deals_data.groupby('month', as_index = False)['dealsPrice'].sum()
	    
	    #Second Output
	    deals_per_contact_data = pd.DataFrame(deals_data.groupby('contactsName', as_index = False)['dealsPrice'].sum())

	    #Third Output
	    sector_rank_data = deals_data.groupby(['month', 'sector'])['dealsPrice'].agg('sum')/deals_data.groupby('month')['dealsPrice'].agg('sum')
	    sector_rank_data = sector_rank_data.reset_index().sort_values(by=['month', 'dealsPrice'], ascending = [True, False])                                                                                           
	    sector_rank_data.rename(columns={'dealsPrice' : 'sector_score'}, inplace = True)

	print('The number of dropped lines is', dropped_lines)

	#MAKE .CSV FILE - 1st OUTPUT
	output_filepath_deals_per_contact = [output_filepath, 'deals_per_contact.csv']
	output_deals_per_contact = '/'.join(output_filepath_deals_per_contact)
	deals_per_contact_data.to_csv(output_deals_per_contact, index = False, encoding='utf-8-sig')

	#MAKE .CSV FILE - 2nd OUTPUT
	output_filepath_deals_per_month = [output_filepath, 'deals_per_month.csv']
	output_deals_per_month = '/'.join(output_filepath_deals_per_month)
	deals_per_month_data.to_csv(output_deals_per_month, index = False, encoding='utf-8-sig')              

	#MAKE .CSV FILE - 3rd OUTPUT
	output_filepath_sector_rank = [output_filepath, 'sector_rank.csv']
	output_sector_rank = '/'.join(output_filepath_sector_rank)
	sector_rank_data.to_csv(output_sector_rank, index = False, encoding='utf-8-sig')


if __name__ == '__main__':
    main() 










