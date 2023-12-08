from typing import List


def prompt_factory(words: List[str], previous_attempts: List[List]) -> str:
    return f"""
    You are playing the popular game "connections". You will be given a multiple of 4
    words up to 16 words, and your task is to find a grouping of 4 words that share
    something in common. The grouping are words that share a common thread. 
    You can only submit a group with words that are contained in the words array and the group
    must not be a group in the previous attempts array.

    Example 1:
    words: [JOHN, CUB, STAR, SILVER, KNEE, THRONE, JOEY, JELLY, CALF, ANKLE, CRAY, HEAD, SHIN, CAN, KID, THIGH]
    previous_attempts: []
    group: [ANKLE, SHIN, KNEE, THIGH]

    Example 2:
    words: [JOHN, CUB, STAR, SILVER, THRONE, JOEY, JELLY, CALF, CRAY, HEAD, CAN, KID]
    previous_attempts: [[JOHN, CUB, STAR, JELLY], [JELLY, CALF, CRAY, HEAD]]
    group: [CALF, CUB, JOEY, KID]

    Example 3:
    words: [CHAD, GEORGIA, JORDAN, TOGO, FISH, GOAT, SCALES, TWINS]
    previous_attempts: [[CHAD, TOGO, FISH, GOAT]]
    group: [FISH, GOAT, SCALES, TWINS]

    Example 4:
    words: [{", ".join(words)}]
    previous_attempts: {"["+ ", ".join(["[" + ", ".join(attempt) + "]" for attempt in previous_attempts]) + "]" if previous_attempts else "[]"}
    group: 
    """
