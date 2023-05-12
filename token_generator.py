import random

numb= ["1", "2", "3", "4", "5", "6", "7" "8", "9", "0"]


num=5


class TokenGenerator:

    def __init__(self) -> None:
        self.initial=0

    @staticmethod
    def generate_token():
        
        my_token=[]
        tokenn=""          
        for my_num in range(1, num+1):
            my_token.append(random.choice(numb))
            

        random.shuffle(my_token)

        for num in my_token:
            self.initial=num
            
            if self.initial


token=TokenGenerator()
tokeenn=token.generate_token()
print(tokeenn)


