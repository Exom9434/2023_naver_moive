import re
import sentencepiece as spm

class Preprocessor:
    def __init__(self, sentences, criteria):
        self.sentences = sentences
        self.criteria = criteria
        
    def labeling(self):
        labeled_data = []
        for sentence, rating in zip(self.sentences, self.criteria):
            label = 1 if rating >= self.criteria else 0
            labeled_data.append((sentence, label))
        return labeled_data
    
    @staticmethod
    def clean_text(text):
        text = re.sub("[^ㄱ-ㅎㅏ-ㅣ가-힣 ]", "", text)
        return text
    
    def preprocess_comments(self):
        processed_sentences = [self.clean_text(sentence) for sentence in self.sentences]
        return processed_sentences
    
    def tokenizer(data,file_name):
        with open(f'{file_name}.txt', 'w', encoding='utf8') as f:
            f.write('\n'.join(data['comment']))
        spm.SentencePieceTrainer.Train(f"--input={file_name}.txt \
                                       --model_prefix={file_name} \
                                       --vocab_size=5000 \
                                       --model_type=bpe\
                                       ")
        comments = {}
        sp = spm.SentencePieceProcessor()
        vocab_file = f"{file_name}.model"
        sp.load(vocab_file)
        for i, comment in enumerate(data["comment"]):
           modified_comments =  sp.encode_as_pieces(comment)
           data["comment"][i] = modified_comments
        
        return data