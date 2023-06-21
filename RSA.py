import random

class RSA:
    def __init__(self, rmin = 1, rmax = 100):
        '''
        rmin / rmax: The minimum / maximum of the range when determining p and q.
                     Use rmin / rmax instead of min / max to avoid overwriting.
                     * rmin should be less than rmax, 
                       otherwise they would be set to default values.
                     * Default values: rmin = 1, rmax = 100
        '''
        self.setRange(rmin, rmax)
        self.ifInit = False
        self.ifSet = False

    def setRange(self, rmin, rmax):
        '''
        - rmin / rmax: The minimum / maximum of the range when determining p and q.
                     Use rmin / rmax instead of min / max to avoid overwriting.
                     * rmin should be less than rmax, 
                       otherwise they would be set to default values.
                     * Default values: rmin = 1, rmax = 100
        - output: True in general.
        '''
        if rmin >= rmax:
            print("rmin is not less than rmax!")
            print("Default valued set.")

            self.rmin = 1
            self.rmax = 100
        else:
            self.rmax = rmax
            self.rmin = rmin

            print("Set successfully.")

        return True
    
    def generate(self):
        '''
        output: A tuple containing two integers.
                The first one is e, and the second one is n.
        '''
        self.ifInit = True

        # select random prime p
        self.p = random.randint(self.rmin, self.rmax)
        while not is_prime(self.p):
            self.p = random.randint(self.rmin, self.rmax)

        # select random prime q
        self.q = random.randint(self.rmin, self.rmax)
        while not is_prime(self.q):
            self.q = random.randint(self.rmin, self.rmax)

        # calculate n and phi
        self.n = self.p * self.q
        self.phi = (self.p - 1) * (self.q - 1)

        # select random key e
        self.e = random.randint(1, self.phi)
        while gcd(self.e, self.phi) != 1:
            self.e = random.randint(1, self.phi)

        for i in range(self.n + 1):
            if self.e * i % self.phi == 1:
                self.d = i
                break

        print("Generated.")
        print("Your public-key is {", self.e, ", ", self.n, "}", sep = '')
        
        return (self.e, self.n)

    def setPartnerKey(self, pt):
        '''
        pt: A tuple containing the partner's e and n, the first element and the second one, respectively.
        output: True if succeeded.
        '''
        if not isinstance(pt, tuple):
            print("Invalid input!")
            return False
        
        if pt[0] >= pt[1]:
            print("e should be less than n!")
            return False

        self.ifSet = True

        self.pe = pt[0]
        self.pn = pt[1]
        print("Set successfully.")

        return True

    def encrypt(self, message):
        '''
        message: Should be a string.
        output: A list containing several integers.
                The list will be empty if failed.
        '''
        if not self.ifSet:
            print("The partner's key has not been set yet!")
            return []

        if not isinstance(message, str):
            print("Invalid message format!")
            return []

        ciphertext = []
        for m in message:
            ln = ord(m) % self.pn # to reduce the difficulty of calculating
            ciphertext.append(ln ** self.pe % self.pn)

        return ciphertext

    def decrypt(self, ciphertext):
        '''
        ciphertext: Should be a list containing several integers.
        output: A string.
                The string will be a empty string if failed.
        '''
        if not self.ifInit:
            print("Not initialized!")
            return ''

        if not isinstance(ciphertext, list):
            print("Invalid message format!")
            return ''

        plaintext = []
        for c in ciphertext:
            plaintext.append(chr(c ** self.d % self.n))

        return ''.join(plaintext)        

    def showKey(self):
        '''
            output: A tuple containing two integers.
                    The first one is e, and the second one is n.
                    It will be empty if not initialized.
        '''
        if not self.ifInit:
            print("Not initialized!")
            return ()
        
        print("Your public-key is {", self.e, ", ", self.n, "}", sep = '')
        return (self.e, self.n)

def is_prime(num):
    if num <= 1:
        return False
    else:
        for n in range(2, num):
            if num % n == 0:
                return False
        return True

def gcd(a, b):
    '''
    it's not necessary to make sure a is greater than b
    since if b is greater than a, a % b will be equal to a
    and gcd(b, a % b) will be gcd(b, a)
    which is what we want initially
    '''
    if a % b == 0:
        return b
    else:
        return gcd(b, a % b)
def main():
        # Initialize two characters.
        sender = RSA()
        receiver = RSA()

        # Generate the public-key of the receiver.
        rpk = receiver.generate()

        # Set the public-key to the sender.
        sender.setPartnerKey(rpk)

        # Encrypting the message.
        message = input("Enter your plaintext: ")
        ciphertext = sender.encrypt(message)

        # Decrypt the message.
        plaintext = receiver.decrypt(ciphertext)

        print("Your message is:\n", plaintext)    
if __name__ == "__main__":
    main()
