document.getElementById("submit").addEventListener("click", function (e) {
  e.preventDefault();
  let longLink = document.getElementById("long-link").ariaValueMax;
  let body = {
    url: longLink,
  };
  if (longLink) {
    fetch("/api", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(body),
    })
      .then((res) => res.json())
      .then((json) => console.log(json));
  }
});
