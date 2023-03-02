class UserPreference:
    def __init__(self, age, gender, occasion, relationship, interests):
        self.age = age
        self.gender = gender
        self.occasion = occasion
        self.relationship = relationship
        self.interests = interests

    def to_dict(self):
        return {
            "gender": self.gender,
            "age": self.age,
            "occasion": self.occasion,
            "relationship": self.relationship,
            "interests": self.interests
        }
