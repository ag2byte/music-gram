function bookmark(songid, isbmd) {
  console.log("Songid: " + songid);
  console.log("IsBMD: " + isbmd);
  //   console.log("USerID: " + userid);

  if (isbmd == "false") {
    fetch("/bookmark", {
      method: "POST",
      body: JSON.stringify({ songid: songid }),

      headers: {
        "Content-type": "application/json;",
      },
    }).then((res) => {
      if (res.status == 201) {
        // all good
        console.log("all good");
        document.getElementById("bom-" + songid).src =
          "https://img.icons8.com/ios-filled/50/000000/bookmark-ribbon.png";
        document
          .getElementById("bom-" + songid)
          .setAttribute("data-bmd", "true");

        // window.location.reload();
      }
    });
  } else if (isbmd == "true") {
    fetch("/unbookmark", {
      method: "POST",
      body: JSON.stringify({ songid: songid }),

      headers: {
        "Content-type": "application/json;",
      },
    }).then((res) => {
      if (res.status == 201) {
        // all good
        console.log("all good");
        document.getElementById("bom-" + songid).src =
          "https://img.icons8.com/ios/50/000000/bookmark-ribbon.png";
        tdocument
          .getElementById("bom-" + songid)
          .setAttribute("data-bmd", "false");
        // window.location.reload();
      }
    });
  }
  window.location.reload();
}
