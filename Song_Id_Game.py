"""
Name: Teng Ian Khoo
Created: 11th August 2019
Last Modified: 23rd August 2019
"""
import re as re


def process(filename):
    """
    This function will process a file of songs into an array of [song_id,word], then using radix sort, sort twice,
    once by the song_id, and because it is a stable sort, once again by word.
    :param filename: a file that holds a song_ids and words associated with that song
    :return: None
    :precondiiton: File exits, the file is made up of a certain format
    :postcondition: A new file is created, containing all the words of all the songs, sorted in lexicographic order
    :complexity: best = worst, O(TM), reading all lines is O(TM), as we have to sort all the words in lexicographic
    order, we will have to use counting sort (O(M)) on all the words, with a upper bound of the longest word, M, T times
    """

    # This is a list that will hold all the song_id + word combinations of the file
    songs_words = []

    # We can at the same time as reading our file, we can calculate the length of our longest song_id,word and num words
    longest_word = 0
    longest_num = 0
    # Opening the file is O(TM) complexity as we have to read all the words in the file, with max word size M
    with open(filename, "r") as file:
        # split each line in the file into an array of [song_id,word_1,word_2......, word_n]
        for line in file:
            words_in_song = re.split('[ :]', line.strip())
            # update the counter for our longest_song_id here for less comparisons
            id_digits = len(words_in_song[0])
            if id_digits > longest_num:
                longest_num = id_digits
            # now for each word in that array we append it into our song_words list as a array[song_id,word], as well
            # as update counters for longest_word
            for i in range(1, len(words_in_song)):
                # update our counter for the longest word in the songs, complexity is O(TM)
                word_length = len(words_in_song[i])
                if word_length > longest_word:
                    longest_word = word_length
                # append our [song_id,word] to our song_words array
                songs_words.append([words_in_song[0], words_in_song[i]])

    # calculate the total number of words in all the files
    total_words = len(songs_words)

    # i will now put each [song_id,word] into a "bucket" depending on the number of digits of their song_id, then
    # radix sort starting from the bucket with the largest digit, then the next largest etc.
    id_bucket = []
    for _ in range(longest_num):
        id_bucket.append([])
    # iterate through all words in the song_words list and append to the appropriate bucket O(T)
    for num in songs_words:
        id_bucket[len(num[0]) - 1].append(num)

    # Now to loop though my bucket_list and radix sort each bucket separately, then combine at the end
    for i in range(longest_num - 1, -1, -1):
        current_bucket = id_bucket[i]
        # if the bucket has 1 or no elements, it is already sorted
        if len(current_bucket) > 1:
            # calculate length of bucket for later use
            current_bucket_length = len(current_bucket)
            # use radix sort for each element in the bucket
            for j in range(i, -1, -1):
                # need to update the variable for current_bucket because it may have changed
                current_bucket = id_bucket[i]
                # initialise the count array
                count_array = [0] * 10
                # populate our count array
                for k in range(current_bucket_length):
                    # populate our count array
                    count_array[int(current_bucket[k][0][j])] += 1
                # Now to construct our position array
                position = [0] * 10
                # initialise 1st position to 1
                position[0] = 1
                # populate the position array
                for x in range(1, len(position)):
                    position[x] = position[x - 1] + count_array[x - 1]
                # construct output
                output = [0] * current_bucket_length
                # loop through the input and sort
                for y in range(current_bucket_length):
                    output[position[int(current_bucket[y][0][j])] - 1] = current_bucket[y]
                    position[int(current_bucket[y][0][j])] += 1
                # now assign the bucket to equal the output
                id_bucket[i] = output

        # Now all buckets should be sorted so we can concat/append all our buckets together
    id_sorted_list = []
    for i in range(len(id_bucket)):
        for item in id_bucket[i]:
            id_sorted_list.append(item)

    songs_words = id_sorted_list

    # Now radix sort my song_words list for letters
    for word_length in range(longest_word - 1, -1, -1):
        # initialise the count_array and a variable to keep track of how many numbers need to be sorted
        count = [0] * 26
        # this variable keeps track of how many items are involved in the current nth letter counting sort
        num_words = 0
        for element in range(total_words):
            # populate the count array and update num_words
            if len(songs_words[element][1]) - 1 >= word_length:
                count[ord(songs_words[element][1][word_length]) - 97] += 1
                num_words += 1
        # construct my position array
        position = [0] * 26
        # initialise my position[0] to equal total_words - num_words
        position[0] = total_words - num_words
        # populate the position array
        for x in range(1, len(position)):
            position[x] = position[x - 1] + count[x - 1]
        # construct output array
        output = [0] * total_words
        word_to_add = 0
        # loop through input and sort the words according to their position array
        for element in range(total_words):
            # check if the current word has enough letters to be sorted
            if len(songs_words[element][1]) - 1 >= word_length:
                output[position[ord(songs_words[element][1][word_length]) - 97]] = songs_words[element]
                position[ord(songs_words[element][1][word_length]) - 97] += 1
            else:
                output[word_to_add] = songs_words[element]
                word_to_add += 1
        # update the song_list variable to now point to the sorted list
        songs_words = output

    # Now that we sorted our file, we can output to a file
    with open("sorted_words.txt", "w+") as f:
        for i in range(len(songs_words)):
            f.write("{0}:{1}\n".format(songs_words[i][1], songs_words[i][0]))


def collate(filename):
    """
    This function will collate all the unique words from a file and write it to a new file, with all the unique words
    and their song_ids
    :return: None, but will write to a file
    :precondiiton: File exits, the file is a file that has been processed by our process function
    :postcondition: A new file is created, containing all the words of all the songs, sorted in lexicographic order
    :complexity: O(TM), we have to look at all the words in
    """
    # This is a list that will hold all the song_id + word combinations of the file
    word_list = []

    # read the file and append it to my word_list
    with open(filename, "r") as file:
        # split each line in the file into an array of [word_n,song_id_n]
        for line in file:
            words_in_song = line.strip().split(":")
            word_list.append(words_in_song)
    # create a list to hold all the unique words
    unique_word_list = []

    # initialise the current_word and current_num to something that we wont find in our file, keep track of the
    # index of our unique_word_list
    current_word = ""
    current_num = ""
    current_index = -1
    # check if i already encountered the word, or number before, then append to my unique_word list
    for i in range(len(word_list)):
        # haven't encountered word before
        if current_word != word_list[i][0]:
            current_word = word_list[i][0]
            current_num = word_list[i][1]
            unique_word_list.append([current_word, current_num])
            current_index += 1
        # if the number changed, then we have to append it to the word_list at the correct index
        elif current_num != word_list[i][1]:
            current_num = word_list[i][1]
            unique_word_list[current_index].append(current_num)

    with open("collated_ids.txt", "w+") as f:
        for i in range(len(unique_word_list)):
            line_to_write = "{0}:".format(unique_word_list[i][0])
            for j in range(1, len(unique_word_list[i])):
                line_to_write = line_to_write + unique_word_list[i][j] + " "
            line_to_write += "\n"
            f.write(line_to_write)


def lookup(collated_file, query_file):
    """
    This function uses binary search to look for
    :param collated_file: A file that has already been processed by the collate function
    :param query_file: A file containing all the queries to look for in the songs
    :return: None, will write to a file the result of the query, the song ids if found, or Not found otherwise
    :complexity: O(q × Mlog(U) + P), q number of queries, M length of longest word, U the number of lines in my
    collated_file and p total number of song_ids in the output
    """
    collate_words = []
    query_words = []

    # read the words from my collated file and add it to my collate_words list
    with open(collated_file, "r") as f:
        for line in f:
            collate_words.append(re.split('[ :]', line.strip()))

    # read the words from my query file and add it to my query_words list
    with open(query_file, "r") as f:
        for line in f:
            query_words.append(line.strip())

    # create an empty string, that will hold all found/Not found results for our queries
    song_ids = ""

    num_words = len(collate_words)
    num_queries = len(query_words)
    # now perform binary search for all of our queries
    for i in range(num_queries):
        # get the word we want to search for
        key = query_words[i]

        low = 0
        high = num_words
        while low < high - 1:
            mid = (low + high) // 2

            if key >= collate_words[mid][0]:
                low = mid
            else:
                high = mid
        # if the key has been found, we we loop through how many elements(times) the word appears and add it to our
        # song_ids string
        if num_queries > 0 and collate_words[low][0] == key:
            for j in range(1, len(collate_words[low])):
                song_ids += collate_words[low][j] + " "
            song_ids += "\n"
        else:
            song_ids += "Not found\n"

    with open("song_ids.txt", "w+") as f:
        f.write(song_ids)

