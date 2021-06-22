import csv
import datetime
import time
import argparse

MAX_VALID_VALUES = 20
FILE_DELIMITER = ','


class InvalidNumberOfValues(Exception):    
    pass

class ValuesAreNonInteger(Exception):    
    pass


def validate_row(row):             
    
    try:
        int_list = [int(x) for x in row]
    except:                
        raise ValuesAreNonInteger

    if len(row) != MAX_VALID_VALUES:
        raise InvalidNumberOfValues

#centralized fizzbuzz logic
def get_fizzbuzz(r, lucky_check = False):
    
    if lucky_check and  '3' in str(r):
        return('lucky')
    elif (int(r) % 3 == 0) and (int(r) % 5 == 0):
        return('fizzbuzz')
    elif  int(r) % 3 == 0:            
        return('fizz')
    elif  int(r) % 5 == 0:            
        return('buzz')        
    else:
        return(str(r).strip())    

#string ouput of fizzbuzz logic
def fizz_buzz_output(row, lucky_check=False):
    output =[]

    for r in row:
         output.append(get_fizzbuzz(r,lucky_check))      
    
    return ' '.join(output)


def fizz_buzz_report(row):
    lucky_counter = 0
    fizz_counter = 0
    buzz_counter = 0
    fizzbuzz_counter = 0
    int_counter = 0 

    for r in row:
        value = get_fizzbuzz(r, lucky_check=True)

        if value == 'lucky':
            lucky_counter +=1
        elif value == 'fizzbuzz':
            fizzbuzz_counter +=1
        elif value == 'fizz':
            fizz_counter +=1
        elif value == 'buzz':
            buzz_counter +=1
        else:
            int_counter +=1

    return f'fizz: {fizz_counter}, buzz: {buzz_counter}, fizzbuzz: {fizzbuzz_counter}, lucky: {lucky_counter}, integer: {int_counter}'


def db_save(run_results, row_results = []):
    from pydblite.sqlite import Database, Table
    #uncomment to store in memory and not persist to disk
    #db = Database(":memory:")
    db = Database("fizzbuzz.db")

    if "run_log" not in db:
        run_log_table = Table('run_log', db)
        run_log_table.create(('run_id', 'INTEGER PRIMARY KEY AUTOINCREMENT' )
                            ,('file_name', 'TEXT NOT NULL' )
                            ,('valid_row_count', 'INTEGER NOT NULL DEFAULT 0')
                            ,('invalid_row_count', 'INTEGER NOT NULL DEFAULT 0')
                            ,('total_row_count', 'INTEGER NOT NULL DEFAULT 0')
                            ,('duration', 'TEXT  NULL')
                            ,('start_time', 'TEXT  NULL')
                            ,('end_time', 'TEXT  NULL'))
    else:
        run_log_table = db["run_log"]

    run_id = run_log_table.insert(file_name=run_results["file_name"]
                                , total_row_count = run_results["total_row_count"]
                                , valid_row_count = run_results["valid_row_count"]
                                , invalid_row_count = run_results["invalid_row_count"]                                
                                , duration = str(run_results["duration"])
                                , start_time = run_results["start_time"]
                                , end_time = run_results["end_time"]
                                )    
    

    record = run_log_table[run_id]

    if "run_row_log" not in db:
        row_log_table = Table('run_row_log', db)
        row_log_table.create(('run_id', 'INTEGER NOT NULL' )
                            ,('row_number', 'INTEGER NOT NULL' )
                            ,('row_input', 'TEXT NOT NULL')
                            ,('error_description', 'TEXT NULL')
                            ,('fizz_buzz_transform1_output', 'TEXT NULL')
                            ,('fizz_buzz_transform2_output', 'TEXT NULL')
                            ,('fizz_buzz_transform3_output', 'TEXT NULL'))
    else:
        row_log_table = db["run_row_log"]                            

    for row in row_results:
        err_desc = None
        fizz_buzz_transform1 = None
        fizz_buzz_transform2 = None
        fizz_buzz_transform3 = None

        if row.get("error_description") != None:
            err_desc = row["error_description"]

        if row.get("fizz_buzz_transform1_output") != None:            
            fizz_buzz_transform1 = row["fizz_buzz_transform1_output"]    

        if row.get("fizz_buzz_transform2_output") != None:
            fizz_buzz_transform2 = row["fizz_buzz_transform2_output"]    

        if row.get("fizz_buzz_transform3_output") != None:
            fizz_buzz_transform3 = row["fizz_buzz_transform3_output"]    

        row_log_table.insert(run_id=run_id
                            , row_number = row["row_number"]
                            , row_input = str(row["row_input"])
                            , error_description = err_desc
                            , fizz_buzz_transform1_output = fizz_buzz_transform1
                            , fizz_buzz_transform2_output = fizz_buzz_transform2
                            , fizz_buzz_transform3_output = fizz_buzz_transform3
                            )    

    run_log_table.commit()
    row_log_table.commit()


def import_file(csv_file_name):

    valid_row_count = 0 
    invalid_row_count = 0 
    row_num  = 0

    #for holding details of run and row level processing
    run_results = {}    
    row_results = []

    run_results["file_name"] = csv_file_name
    run_results["start_time"] = datetime.datetime.now()

    with open(csv_file_name,'r') as csv_file:        
        csv_reader = csv.reader(csv_file, delimiter=FILE_DELIMITER)
        
        run_results["file_name"] = csv_file_name
        
        for row in csv_reader:            
            row_num += 1
            row_result = {}
            row_result["row_number"] = row_num
            row_result["row_input"] = row

            try:
                validate_row(row)
                row_result["fizz_buzz_transform1_output"] =  fizz_buzz_output(row)  
                row_result["fizz_buzz_transform2_output"] =  fizz_buzz_output(row, lucky_check=True)  
                row_result["fizz_buzz_transform3_output"] =  fizz_buzz_report(row)  
                valid_row_count += 1
            except InvalidNumberOfValues:            
                invalid_row_count += 1 
                row_result["error_description"] = "Invalid number of columns"                
            except ValuesAreNonInteger:            
                invalid_row_count += 1 
                row_result["error_description"] = "Row contains non Integer values"
            
            row_results.append(row_result)
            

    run_results["total_row_count"] = row_num 
    run_results["valid_row_count"] = valid_row_count
    run_results["invalid_row_count"] = invalid_row_count
    run_results["end_time"] = datetime.datetime.now()
    run_results["duration"] = run_results["end_time"] - run_results["start_time"]

    db_save(run_results, row_results)

    return run_results


def main(file_name):
        
    result = import_file(file_name)    
    print(f"Valid Rows:= {result['valid_row_count']} | Invalid Rows:= {result['invalid_row_count']} - in {result['duration'].total_seconds()} seconds")

if __name__ == "__main__":
    file_name = './data/test_values.csv'

    parser = argparse.ArgumentParser()
    parser.add_argument("-f", "--filename", help="name of inputfile to process")    
    args = parser.parse_args()    

    if args.filename:
        file_name = args.filename

    main(file_name)
