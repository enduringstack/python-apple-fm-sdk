/*
For licensing see accompanying LICENSE file.
Copyright (C) 2026 Apple Inc. All Rights Reserved.
*/

import FoundationModels

// Simple example
@Generable
struct Age {
  var years: Int
  var months: Int
}

// Simple example with nested property
@Generable(description: "A description of a cute cat")
struct Cat {
  var age: Age
  var name: String
  var profile: String
}

// Next simplest: added complexity of Guides
@Generable
struct Hedgehog {
  @Guide(description: "A cute old-timey name")
  var name: String

  @Guide(description: "The hedgehog's age", .range(0...8))
  var age: Int

  @Guide(description: "The hedgehog's favorite food", .anyOf(["carrot", "turnip", "leek"]))
  var favoriteFood: String

  @Guide(.constant("a hedge"))
  var home: String

  @Guide(description: "The hedgehog's hobbies", .count(3))
  var hobbies: [String]
}

// An example that wraps a different generable type
@Generable
struct Shelter {
  var cats: [Cat]
}

// This is a more complex example because it's nested
@Generable
struct Person {
  @Guide(description: "The person's age", .range(18...100))
  var age: Int?

  @Guide(description: "The person's children", .maximumCount(3))
  var children: [Person]

  @Guide(description: "The person's name")
  var name: String
}

// An extra-complex example that references multiple generable types
@Generable
struct PetClub {
  var members: [Person]
  var cats: [Cat]
  var hedgehogs: [Hedgehog]
  var otherPets: [String]

  @Guide(description: "Should be the name of one of the members")
  var presidentName: String
}

// An extra-complex example with optional properties
@Generable
struct ShelterNewsletter {
  let title: String

  let topic: String

  @Guide(description: "A local company that's sponsoring this newsletter, if applicable")
  let sponsor: String?

  let issueNumber: Int?

  @Guide(description: "Search keywords for this newsletter")
  let tags: [String]?

  let featuredCats: [Cat]?

  let featuredHedgehog: Hedgehog?

  let featuredStaff: [Person]?
}
