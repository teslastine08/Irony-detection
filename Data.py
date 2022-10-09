review2014_path = "C:/Users/admin/Desktop/data.csv.csv"
truth_file = os.listdir(blog2014_path)[-1]
reviews_truth_df = pd.read_csv(review2014_path+truth_file, sep=":::", header=None, names=('file','gender','age'))
# print truth_df.columns.values
reviews_truth_df = reviews_truth_df.set_index('file')
review_df = pd.DataFrame(columns=('file', 'text', 'gender', 'age'))
count = 0
for file in review2014_files:
    author = {}
    author['file'] = file[:-4]
    #print file
    with open(review2014_path+file) as f:
        tree = ET.parse(f)
        raw_text = []        
        for node in tree.iter('document'):
            raw_text.append(BS(node.text, 'html.parser').get_text().strip())
        author['text'] = '\n'.join(raw_text)
        author['gender'] = reviews_truth_df.loc[author['file']]['gender']
        #print author['gender']
        author['age'] = reviews_truth_df.loc[author['file']]['age']
    author_series = pd.Series(author)
    author_series.name = author['file']
#     author_series =  pd.Series(dict(zip(['file', 'text', 'gender', 'age'], [author['file'],author['text'],author['gender'],author['age']])))
    author_series.name = author['file']
    review_df = review_df.append(author_series)
    count += 1
    if count%50 == 0:
        print (count," records processed")
review_df['MRC_POS'] = find_MRC_POS(review_df['text'])
review_df.head()
