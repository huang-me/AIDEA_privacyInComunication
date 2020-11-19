# Load file and format the contents
# 
#         肝 O
#         功 O
#         能 O
#         6 B-med_exam
#         8 I-med_exam

import os

def formatfile(filehead):
    inputfile = filehead + '.txt'
    outputfile = filehead + '.out'
    
    trainingset = []
    position = []
    mentions = {}
    
    with open(inputfile, 'r', encoding='utf-8') as file:
        datas = file.read().encode('utf-8').decode('utf-8-sig')
    # SPLIT DIFFIERENT CONTENTS
    datas = datas.split('\n\n--------------------\n\n')[:-1]
    # GET ALL INFORMATIONS FROM DATA
    for data in datas:
        data = data.split('\n')
        trainingset.append(data[0])
        annotations = data[1:]
        for annot in annotations[1:]:
            annot = annot.split('\t')
            position.extend(annot)
            mentions[annot[3]] = annot[4]
            
    if os.path.isfile(outputfile):
        os.remove(outputfile)
    outfile = open(outputfile, 'a', encoding='utf-8')
    
    # output file lines
    count = 0 # annotation counts in each content
    tagged = list()
    cnt = 0
    for article_id in range(len(trainingset)):
        trainingset_split = list(trainingset[article_id])
        while '' or ' ' in trainingset_split:
            if '' in trainingset_split:
                trainingset_split.remove('')
            else:
                trainingset_split.remove(' ')
        start_tmp = 0
        for position_idx in range(0,len(position),5):
            if int(position[position_idx]) == article_id:
                count += 1
                if count == 1:
                    start_pos = int(position[position_idx+1])
                    end_pos = int(position[position_idx+2])
                    entity_type=position[position_idx+4]
                    if start_pos == 0:
                        token = list(trainingset[article_id][start_pos:end_pos])
                        whole_token = trainingset[article_id][start_pos:end_pos]
                        for token_idx in range(len(token)):
                            if len(token[token_idx].replace(' ','')) == 0:
                                continue
                            # BIO states
                            if token_idx == 0:
                                label = 'B-'+entity_type
                            else:
                                label = 'I-'+entity_type
                            
                            output_str = token[token_idx] + ' ' + label + '\n'
                            outfile.write(output_str)

                    else:
                        token = list(trainingset[article_id][0:start_pos])
                        whole_token = trainingset[article_id][0:start_pos]
                        for token_idx in range(len(token)):
                            if len(token[token_idx].replace(' ','')) == 0:
                                continue
                            
                            output_str = token[token_idx] + ' ' + 'O' + '\n'
                            outfile.write(output_str)

                        token = list(trainingset[article_id][start_pos:end_pos])
                        whole_token = trainingset[article_id][start_pos:end_pos]
                        for token_idx in range(len(token)):
                            if len(token[token_idx].replace(' ','')) == 0:
                                continue
                            # BIO states
                            if token[0] == '':
                                if token_idx == 1:
                                    label = 'B-'+entity_type
                                else:
                                    label = 'I-'+entity_type
                            else:
                                if token_idx == 0:
                                    label = 'B-'+entity_type
                                else:
                                    label = 'I-'+entity_type

                            output_str = token[token_idx] + ' ' + label + '\n'
                            outfile.write(output_str)

                    start_tmp = end_pos
                else:
                    start_pos = int(position[position_idx+1])
                    end_pos = int(position[position_idx+2])
                    entity_type=position[position_idx+4]
                    if start_pos<start_tmp:
                        continue
                    else:
                        token = list(trainingset[article_id][start_tmp:start_pos])
                        whole_token = trainingset[article_id][start_tmp:start_pos]
                        for token_idx in range(len(token)):
                            if len(token[token_idx].replace(' ','')) == 0:
                                continue
                            output_str = token[token_idx] + ' ' + 'O' + '\n'
                            outfile.write(output_str)

                    token = list(trainingset[article_id][start_pos:end_pos])
                    whole_token = trainingset[article_id][start_pos:end_pos]
                    for token_idx in range(len(token)):
                        if len(token[token_idx].replace(' ','')) == 0:
                            continue
                        # BIO states
                        if token[0] == '':
                            if token_idx == 1:
                                label = 'B-'+entity_type
                            else:
                                label = 'I-'+entity_type
                        else:
                            if token_idx == 0:
                                label = 'B-'+entity_type
                            else:
                                label = 'I-'+entity_type
                        
                        output_str = token[token_idx] + ' ' + label + '\n'
                        outfile.write(output_str)
                        
                    start_tmp = end_pos

        token = list(trainingset[article_id][start_tmp:])
        whole_token = trainingset[article_id][start_tmp:]
        for token_idx in range(len(token)):
            if len(token[token_idx].replace(' ','')) == 0:
                continue

            
            output_str = token[token_idx] + ' ' + 'O' + '\n'
            outfile.write(output_str)

        count = 0
    
        output_str = '\n'
        outfile.write(output_str)

        if article_id%10 == 0:
            print('Total complete articles:', article_id)

    # close output file
    outfile.close()

# Check if the input file has been formatted

import os
def checkfile(filehead):
    filepath = filehead + '.out'
    if not os.path.isfile(filepath):
        filein = filehead + '.txt'
        formatfile(filehead)

# Load the .out file and return lists

def load_out(filehead):
    filepath = filehead + '.out'
    with open(filepath, 'r', encoding='utf-8') as infile:
        datas = infile.readlines()
    datalist = []
    datalist_tmp = []
    tags = []
    tags_tmp = []
    id = 0

    for row in datas:
        if row == '\n':
            id += 1
            datalist.append(datalist_tmp)
            datalist_tmp = []
            tags.append(tags_tmp)
            tags_tmp = []
        else:
            row = row.strip('\n').split(' ')
            datalist_tmp.append(row[0])
            tags_tmp.append(row[1])
    if len(datalist_tmp) != 0:
        datalist.append(datalist_tmp)
        tags.append(tags_tmp)

    return datalist, tags

# Load the predict file

def loadpred(predfile):
    content = []
    with open(predfile, 'r', encoding='utf-8') as f:
        datas = f.read()
    datas = datas.split('\n\n--------------------\n\n')[:-1]
    for data in datas:
        data = data.split('\n')
        content.append(list(data[1]))
    return content

# Format output

def output(dta, y_pred):
    output="article_id\tstart_position\tend_position\tentity_text\tentity_type\n"
    for test_id in range(len(y_pred)):
        pos=0
        start_pos=None
        end_pos=None
        entity_text=None
        entity_type=None
        for pred_id in range(len(y_pred[test_id])):
            if y_pred[test_id][pred_id][0]=='B':
                start_pos=pos
                entity_type=y_pred[test_id][pred_id][2:]
            elif start_pos is not None and y_pred[test_id][pred_id][0]=='I' and                     (len(y_pred[test_id])-1==pred_id or y_pred[test_id][pred_id+1][0]=='O'):
                end_pos=pos
                entity_text=''.join([dta[test_id][position] for position in range(start_pos,end_pos+1)])
                line=str(test_id)+'\t'+str(start_pos)+'\t'+str(end_pos+1)+'\t'+entity_text+'\t'+entity_type
                output+=line+'\n'
            pos+=1
    output_path = 'output.tsv'
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(output)