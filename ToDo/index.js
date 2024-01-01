import express from "express";
import bodyParser from "body-parser";
import mongoose from "mongoose";

const app = express();
app.set("view engine", "ejs"); // Set EJS as the view engine

app.use(express.static("public"));
app.use(bodyParser.urlencoded({ extended: true }));

mongoose.connect('mongodb://127.0.0.1:27017/todolistDB', { useNewUrlParser: true, useUnifiedTopology: true })
  .then(() => {
    console.log('Connected to MongoDB');
  })
  .catch(err => {
    console.error('Error connecting to MongoDB:', err);
  });

const itemsSchema = {
  name: String
};

const Item = mongoose.model("Item", itemsSchema);

const defaultItems = [
  new Item({ name: "Eat food" }),
  new Item({ name: "Drink water" }),
  new Item({ name: "Deep breaths" })
];

const listSchema = {
  name: String,
  items: [itemsSchema]
};

const List = mongoose.model("List", listSchema);

async function fetchData() {
  try {
    const foundItems = await Item.find({});
    return foundItems;
  } catch (err) {
    console.error('Error fetching items:', err);
    return [];
  }
}

app.get("/", async function(req, res) {
  const foundItems = await fetchData();

  if (foundItems.length === 0) {
    await Item.insertMany(defaultItems);
    res.redirect("/");
  } else {
    res.render("index.ejs", { listTitle: "Today", foundItems }); // Provide a default title
  }
});

app.post("/add", async function(req, res) {
  const itemName = req.body.newItem;
  const listName = req.body.button;
  const item = new Item({ name: itemName });

  if (listName === "Today") {
    await item.save();
    res.redirect("/");
  } else {
    try {
      const foundList = await List.findOne({ name: listName });

      if (foundList) {
        foundList.items.push(item);
        await foundList.save();
      } else {
        const newList = new List({
          name: listName,
          items: [item]
        });
        await newList.save();
      }

      res.redirect("/" + listName);
    } catch (err) {
      console.error("Error occurred:", err);
      res.status(500).send("An error occurred while processing the request.");
    }
  }
});

app.post("/delete", async function(req, res) {
  const deleteItemId = req.body.id;
  const listName = req.body.listName;

  try {
    if (listName === "Today") {
      await Item.findByIdAndRemove(deleteItemId);
      console.log("Item deleted successfully");
      res.redirect("/");
    } else {
      const updatedList = await List.findOneAndUpdate(
        { name: listName },
        { $pull: { items: { _id: deleteItemId } } }
      );
      if (updatedList) {
        res.redirect("/" + listName);
      } else {
        console.error("List not found");
        res.status(500).send("An error occurred while updating the list");
      }
    }
  } catch (err) {
    console.error(err);
    res.status(500).send("An error occurred");
  }
});


app.get("/:customName", async function(req, res) {
  try {
    const customListName = req.params.customName;
    const foundList = await List.findOne({ name: customListName });

    if (!foundList) {
      const newList = new List({
        name: customListName,
        items: defaultItems
      });
      await newList.save();
      res.render("index.ejs", { listTitle: customListName, foundItems: defaultItems });
    } else {
      res.render("index.ejs", { listTitle: foundList.name, foundItems: foundList.items });
    }
  } catch (err) {
    console.error("Error occurred:", err);
    res.status(500).send("An error occurred while processing the request.");
  }
});

app.listen(3000, function() {
  console.log("Server started on port 3000");
});
