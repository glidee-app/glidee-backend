import random

letters= ("a b c d e f g h i j k l m n o p q r s t u v w x y z A B C D E F G H I J K L M N O P Q R S T U V W X Y Z")

letter=letters.split(" ")

numb= ["1", "2", "3", "4", "5", "6", "7" "8", "9", "0"]
letter_num=3

num=5


class TokenGenerator:

    @staticmethod
    def generate_token():
        
        my_token=[""]
        tokenn=""
        for my_letter in range(1, letter_num+1):
            my_token.append(random.choice(letter))
            
        for my_num in range(1, num+1):
            my_token.append(random.choice(numb))
            

        random.shuffle(my_token)
        token=tokenn.join(my_token)
        return (token)


