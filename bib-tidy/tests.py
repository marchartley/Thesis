import re
#
# def isMail(s):
#     # return re.match(r".*@.*", s) is not None
#     return re.match(r"^[0-9a-zA-Z.]+@.*(\.fr|\.com|\.org)$", s) is not None
#
# print(isMail("marctest.fr"))
# print(isMail("marc@test.fr"))
# print(isMail("marc.h@test.fr"))
# print(isMail("mArc32@test.frz"))
# print(isMail("mar]c@test.frz"))

def test(s):
    return re.findall(r"^([a-z]{2,3})(\d{1,4})\1$", s)


print(test("abc12abcef"))
print(test("ac1ac"))
print(test("aca1ac"))
print(test("ac1354ac"))