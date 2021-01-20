import argparse
import json
import MeCab

from wordcloud import WordCloud
from collections import defaultdict

DEL_LIST = ['の', '削除', '済み', '動画']

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--json-path', type=str, default='./watch-history.json')
    parser.add_argument('--font-path', type=str, default='/System/Library/Fonts/ヒラギノ角ゴシック W4.ttc')
    parser.add_argument('--width', type=int, default=1920)
    parser.add_argument('--height', type=int, default=1080)
    parser.add_argument('--max-words', type=int, default=400)
    parser.add_argument('--dst', type=str, default='./result.png')
    
    return parser.parse_args()

def main():
    args = parse_args()
    with open(args.json_path, 'r') as f:
        history = json.load(f)

    title_list = [entry['title'].replace('を視聴しました', ' ') for entry in history]
    title_list = [title for title in title_list if not 'https' in title]

    word_list = list()

    mecab = MeCab.Tagger('-Ochasen')
    mecab.parse('')

    for title in title_list:
        node = mecab.parseToNode(title)
        while node:
            word = node.surface
            pos = node.feature.split(',')
            if (pos[0] in ['名詞']) and (word not in DEL_LIST):
                word_list.append(word)
            node = node.next

    count = defaultdict(int)
    for word in word_list:
        count[word] += 1

    ranking = sorted(count.items(), key=lambda x: x[1])

    wordcloud = WordCloud(background_color='white',
            font_path=args.font_path, 
            width=args.width, height=args.height,
            max_words=args.max_words).generate(' '.join(word_list))
    wordcloud.to_file(args.dst)

if __name__ == '__main__':
    main()

