import pypyodbc as pdbc
import pandas as pd
from pandas import DataFrame, Series
import pytz
from pytz import timezone
from datetime import datetime
from fuzzy_adventure.hana import connection
import tarfile
import os
from os import listdir
import re
import csv
import time


def get_timestamp_fields():
    cursor.execute("""select * from TABLE_COLUMNS where "SCHEMA_NAME"='MIMIC2' and "DATA_TYPE_NAME"='TIMESTAMP' order by "TABLE_NAME", "POSITION" """)
    rows = cursor.fetchall()
    headers = DataFrame(cursor.description)

    timestamp_field_df = DataFrame(rows, columns = headers[0])
    return timestamp_field_df


def timestamp_processing(file_path, table):

    ts_columns = timestamp_df[timestamp_df.table_name == table].column_name.values
    if os.path.getsize(file_path) > 0:
        #na_filter=False because Pandas tries to figure out what the type of a column is and if they're all
        #integer except one (null value), it converts it to float. That interfers with HANA's ability to import
        #integers since it reads a float, no conversion done.
        df = pd.read_csv(file_path, na_filter=False) 
    else:
        return None

    if table in tables_with_timestamps:
        for col_name in ts_columns:
            #Apply the most import part, date conversion to UTC
            df[col_name.upper()] = df[col_name.upper()].apply(to_utc)

    #Fill the void with null. Easier to import 'null' values in HANA through csv files
    df = df.applymap(fill_void)

    return df


def fill_void(value):
    if value == '':
        return 'null'
    return value


def to_utc(date_string):

    fmt_with_tz = '%Y-%m-%d %H:%M:%S %Z'

    try:
        datetime.strptime(date_string, fmt_with_tz)
    except:
        return date_string

    tz = date_string[-3:]

    utc = pytz.utc
    local = None
    if tz == 'EST':
        local = timezone('US/Eastern')
    else:
        local = timezone('US/Eastern')
        print tz

    fmt = '%Y-%m-%d %H:%M:%S'
    date = date_string[:-4]
    dt = local.localize(datetime.strptime(date, fmt))

    utc_dt = dt.astimezone(utc)

    return utc_dt.strftime(fmt)

def untar(path):
    tar = tarfile.open(path)
    tar.extractall()
    tar.close()


def make_tarfile(output_filename, source_dir):
    with tarfile.open(output_filename, "w:gz") as tar:
        tar.add(source_dir, arcname=os.path.basename(source_dir))


def insert_definition_files():
    untar(slices_path + definition_file)

    for definition in listdir('Definitions'):
        df = pd.read_csv(slices_path + 'Definitions/' + definition, header=None, skiprows=1)

        num_line = df[0].count()
        size = df.ix[0].size

        query = """INSERT INTO "MIMIC2"."mimic.tables::?" VALUES ("""

        for i in range(size):
            query += '?,'

        query = query[:-1] + ')'

        table = re.split("\.txt",definition)[0].lower()

        for i in range(num_line):
            conn.execute(query % ((table,) + tuple(df.ix[i].tolist())))



if __name__ == '__main__':
    
    conn = pdbc.connect('DSN=hana; UID=ALEXIS; PWD=Arkham3!')
    cursor = conn.cursor() #connection.get_cursor()


    slices_path = '/home/shared/MIMIC/data_slices/'
    slices_base_name = 'mimic2cdb-2.6-%s.tar.gz'
    table_base_name = 'mimic.tables::'
    definition_file = 'mimic2cdb-2.6-Definitions.tar.gz'

    timestamp_df = get_timestamp_fields()
    tables_with_timestamps = timestamp_df.table_name.unique()

    import_slices = open('import slices.txt', 'w')
    for slice_number in range(33):
        start = time.time()
        if slice_number < 10:
            slice_number = '0' + str(slice_number)
        data_slice_path = slices_path + slices_base_name % str(slice_number)

        # Untar slice
        untar(data_slice_path)

        for (n, patient) in enumerate(listdir(str(slice_number))):
            records_dict = {}

            for record in listdir(str(slice_number) + '/' + patient):
                record_name = re.split("-[0-9]{5,5}\.txt",record)[0].lower()
                table = table_base_name + record_name

                path = str(slice_number) + '/' + patient + '/' + record

                processed_df = timestamp_processing(path, table)
                
                if processed_df is None:
                    continue

                processed_df.to_csv(path, index=False, line_terminator='@@\n')

                records_dict[record_name] = "import from csv file '/home/share/mimic/" + path + "'" + 'into "MIMIC2"."' + table + '" with skip first 1 row record delimited by \'@@\\n\''

            for record in ['d_patients', 'icustayevents', 'admissions', 'poe_order', 'icustay_days', 'comorbidity_scores', 'demographic_detail','icustay_detail']:

                if record in records_dict.keys():
                    import_slices.write(records_dict[record] + '\n')
                    del records_dict[record]

            for record in records_dict.keys():
                import_slices.write(records_dict[record] + '\n')



        make_tarfile(slices_base_name % slice_number, str(slice_number))
        end = time.time()

        print "Slice " + str(slice_number) + " | " + str(end - start)
    import_slices.close()


