from django.core.management.base import BaseCommand
from tqdm import tqdm
from vocabulary.models import Source, Definition, Vocabulary
from vocabulary.scrapper import get_word


class Command(BaseCommand):
    help = 'Get all the vocabulary From vocabulary.com'

    def handle(self, *args, **kwargs):
        source = Source.objects.get(title='vocabulary.com')
        with open('words.txt', 'r') as file:
            words = file.readlines()

        for word in tqdm(words):
            word = word.strip()
            get_this_word = Vocabulary.objects.filter(word_name=word)
            if get_this_word:
                continue
            obj = get_word(word)
            if not obj:
                continue
            get_this_word = Vocabulary.objects.filter(word_name=obj['original_word'])
            if get_this_word:
                continue

            vocabulary = Vocabulary(
                word_name=obj['original_word'],
                short_definition=obj['short_def'],
                long_definition=obj['long_def'],
                american_phonetic=obj['american_phonetic'],
                british_phonetic=obj['british_phonetic'],
                american_audio_url=obj['american_audio_url'],
                british_audio_url=obj['british_audio_url'],
            )
            vocabulary.save()

            for my_def in obj['defs']:
                definition = Definition(
                    word=vocabulary,
                    part_of_speech=my_def[0],
                    definition=my_def[1],
                    type='en',
                    source=source
                )
                definition.save()
