import os
import sys
import socket
import tensorflow as tf

from settings import PROJECT_ROOT 
from chatbot.botpredictor import BotPredictor

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'

def main() :

    corp_dir = os.path.join(PROJECT_ROOT, 'Data', 'Corpus')
    knbs_dir = os.path.join(PROJECT_ROOT, 'Data', 'KnowledgeBase')
    res_dir = os.path.join(PROJECT_ROOT, 'Data', 'Result')

    with tf.Session() as sess:
        predictor = BotPredictor(sess, corpus_dir=corp_dir, knbase_dir=knbs_dir,
                                 result_dir=res_dir, result_file='basic-32334')

        sock=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        host = '127.0.0.1'
        port = int(2000)
        sock.bind((host, port))
        sock.listen(1)
        print("chatServer Start...\n")
        while True:
            connection, client_addr = sock.accept()
            # print(connection, client_addr)
            data = connection.recv(1024)
            data = data.decode("utf-8")
            print("data > "+data)

    	    # This command UI has a single chat session only
            session_id = predictor.session_data.add_session()
            question = data
            if question.strip() == 'exit':
                print("Thank you for using HeroBot. Goodbye.")
                break
            answer = predictor.predict(session_id, question)
            print("answ > "+answer)
            connection.sendall(answer.encode("utf-8"))
            connection.close()
        sock.close()
if __name__ == "__main__" :
    main()