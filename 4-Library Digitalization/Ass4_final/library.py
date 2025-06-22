import hash_table as ht

class DigitalLibrary: 
    def __init__(self):
        pass 
    def distinct_words(self, book_title):
        pass
    def count_distinct_words(self, book_title):
        pass
    def search_keyword(self, keyword):
        pass
    def print_books(self):
        pass
    
class MuskLibrary(DigitalLibrary):  

    def __init__(self, book_titles, texts):
        self.books = []
        for i in range(len(book_titles)):
            temp1 = book_titles[i]
            temp2 =[]
            for t in texts[i]:
                temp2.append(t)
            self.books.append([temp1, temp2])
        self.merge_sort_books(self.books)
        for i in range(len(self.books)):
            self.merge_sort(self.books[i][1])

        self.cnt_diff_word = [] 
        self.diff_word = []
        for i in range(len(self.books)):
            cnt = 0
            temp = []
            for j in range(len(self.books[i][1])):
                if j == 0:
                    cnt += 1
                    temp.append(self.books[i][1][j])
                elif self.books[i][1][j] != self.books[i][1][j-1]:
                    cnt += 1
                    temp.append(self.books[i][1][j])
            self.cnt_diff_word.append([self.books[i][0], cnt])
            self.diff_word.append([self.books[i][0], temp])
             
    def merge_sort(self, words):
        if len(words) > 1:
            mid = len(words) // 2
            left_half = words[:mid]
            right_half = words[mid:]

            self.merge_sort(left_half)
            self.merge_sort(right_half)

            i = j = k = 0

            while i < len(left_half) and j < len(right_half):
                if left_half[i] < right_half[j]:
                    words[k] = left_half[i]
                    i += 1
                else:
                    words[k] = right_half[j]
                    j += 1
                k += 1

            while i < len(left_half):
                words[k] = left_half[i]
                i += 1
                k += 1

            while j < len(right_half):
                words[k] = right_half[j]
                j += 1
                k += 1
        return
    
    def merge_sort_books(self, books):
        if len(books) > 1:
            mid = len(books) // 2
            left_half = books[:mid]
            right_half = books[mid:]

            self.merge_sort_books(left_half)
            self.merge_sort_books(right_half)

            i = j = k = 0

            while i < len(left_half) and j < len(right_half):
                if left_half[i][0] < right_half[j][0]:
                    books[k] = left_half[i]
                    i += 1
                else:
                    books[k] = right_half[j]
                    j += 1
                k += 1

            while i < len(left_half):
                books[k] = left_half[i]
                i += 1
                k += 1

            while j < len(right_half):
                books[k] = right_half[j]
                j += 1
                k += 1

        return

    def distinct_words(self, book_title): 
        l = 0
        r = len(self.books) - 1 
        index = None
        while l <= r:
            mid = (l + r) // 2
            if self.books[mid][0] == book_title: 
                index = mid
                break
            elif self.books[mid][0] < book_title:
                l = mid + 1
            else:
                r = mid - 1

        return self.diff_word[index][1] 
    
    def count_distinct_words(self, book_title): 
        l = 0
        r = len(self.books) - 1 
        index = None
        while l <= r:
            mid = (l + r) // 2
            if self.books[mid][0] == book_title: 
                index = mid
                break
            elif self.books[mid][0] < book_title:
                l = mid + 1
            else:
                r = mid - 1

        return self.cnt_diff_word[index][1]  
    
    def search_keyword(self, keyword): 
        ans = []
        for i in range(len(self.books)):
            l = 0
            r = len(self.books[i][1]) - 1
            while l <= r:
                mid = (l + r) // 2
                if self.books[i][1][mid] == keyword:
                    ans.append(self.books[i][0])
                    break
                elif self.books[i][1][mid] < keyword:
                    l = mid + 1
                else:
                    r = mid - 1
        return ans 
    
    def print_books(self):
        for i in range(len(self.diff_word)):
            print(self.diff_word[i][0] , end=": ")
            for j in range(len(self.diff_word[i][1])):
                if j == len(self.diff_word[i][1]) - 1:  print(self.diff_word[i][1][j],end="")
                else:                                   print(self.diff_word[i][1][j],end=" | ")
            print()

class JGBLibrary(DigitalLibrary): 
    def __init__(self, name, params): 
        self.params = params 
        if name == "Jobs":      self.collision_type = "Chain"
        elif name == "Gates":   self.collision_type = "Linear"
        else:                   self.collision_type = "Double"
        self.mp = ht.HashMap(self.collision_type, params) 
        self.books = []

    def add_book(self, book_title, text): 
        self.books.append(book_title)
        st = ht.HashSet(self.collision_type,self.params)
        for i in range(len(text)):
            st.insert(text[i])
        self.mp.insert([book_title,st]) 
    
    def distinct_words(self, book_title):
        an = []
        st = self.mp.find(book_title)
        if st == None:
            raise ValueError("NO BOOK FOUND")  
        if self.collision_type == "Chain":
            for i in range(len(st.table)):
                if st.table[i] != None:
                    for j in range(len(st.table[i])):
                        an.append(st.table[i][j])
            return an
        for i in range(len(st.table)):
            if st.table[i] != None:
                an.append(st.table[i])
        return an
    
    def count_distinct_words(self, book_title):
        if self.mp.find(book_title) == None:
            raise ValueError("NO BOOK FOUND")  
        return self.mp.find(book_title).num_of_elements

    def search_keyword(self, keyword): 
        an = []
        for i in range(len(self.books)):
            if self.mp.find(self.books[i]) == None: 
                continue
            elif self.mp.find(self.books[i]).find(keyword)==True:
                an.append(self.books[i])
        return an
        
    def print_books(self): 
        if self.collision_type == "Chain":
            for i in range(len(self.mp.table)):
                if self.mp.table[i] != None:
                    for j in range(len(self.mp.table[i])):
                        print(self.mp.table[i][j][0],end=": ")
                        print(self.mp.table[i][j][1],end="")
                        print()
        else:
            for i in range(len(self.mp.table)):
                if self.mp.table[i] != None:
                    print(self.mp.table[i][0],end=": ")
                    print(self.mp.table[i][1],end="")
                    print()