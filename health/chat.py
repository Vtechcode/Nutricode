import openai
from decouple import config

def open_file(filepath):
    with open(filepath, 'r', encoding = 'utf-8') as infile:
        return infile.read()

openai.api_key = config('OPEN_AI_KEY')

def gpt3_completion(prompt, engine ='text-davinci-002', temp = 0.7, top_p = 1.0, tokens = 400, freq_pen = 0.0, pres_pen = 0.0, stop = ['NAWI:', 'USER:']):
    prompt = prompt.encode(encoding = 'ASCII', errors = 'ignore').decode()
    response = openai.Completion.create(
        engine = engine,
        prompt = prompt,
        temperature = temp,
        max_tokens = tokens,
        top_p = top_p,
        frequency_penalty = freq_pen,
        presence_penalty = pres_pen,
        stop = stop
    )
    text = response['choices'][0]['text'].strip()
    return text


if __name__ == '__main__':
    conversation = list()
    print('NAWI: Hi there! How may I help you today?')
    while True:
        user_input = input('\nUSER: ')
        conversation.append('USER: %s' % user_input)
        text_block = '\n'.join(conversation)
        prompt = open_file('health/prompt_chat.txt').replace('<<BLOCK>>', text_block)
        prompt = prompt + '\nNAWI:'
        response = gpt3_completion(prompt)
        print('\nNAWI:', response)
        conversation.append('NAWI: %s' % response)