import mongoose from "mongoose";

async function main() {
  try {
    // Connect to the MongoDB server
    await mongoose.connect("mongodb://127.0.0.1:27017/fruitsDB", {
      useNewUrlParser: true,
      useUnifiedTopology: true
    });

    // Define the fruit schema
    const fruitSchema = new mongoose.Schema({
      name: String,
      rating: {
        type: Number,
        min: 1,
        max: 10,
      },
      review: String
    });

    // Create the Fruit model
    const Fruit = mongoose.model("Fruit", fruitSchema);

    // Create an array of fruit instances
    const fruitsToInsert = [
      {
        name: "Apple",
        rating: 4,
        review: "Very good but could be better"
      },
      {
        name: "Banana",
        rating: 5,
        review: "Very good"
      },
      {
        name: "Orange",
        rating: 6,
        review: "Good, sometimes"
      }
    ];

    // Insert the array of fruits into the database
    // await Fruit.insertMany(fruitsToInsert);
    console.log("Fruits saved successfully!");

    // Query and display fruits
    const fruits = await Fruit.find(); // Find all fruits
    fruits.forEach(function(fruit) {
      console.log(fruit.name);
    });

    // Update a fruit
    await Fruit.updateOne(
      { _id: "64d7a164096f141ce23b964f" },
      { rating: "Idk what fruit" },

    );
    console.log("Fruit updated successfully!");
  } catch (error) {
    console.error("Error:", error);
  } finally {
    // Close the database connection
    mongoose.disconnect();
  }
}

main();
