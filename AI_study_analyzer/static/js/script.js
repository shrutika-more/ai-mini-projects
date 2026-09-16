async function generateAI() {

    const task = document.getElementById("task").value;
    const text = document.getElementById("text").value;

    const result = document.getElementById("result");
    const loading = document.getElementById("loading");
    const button = document.getElementById("generateBtn");

    // Check input
    if (text.trim() === "") {

        alert("Please enter a topic or text.");

        return;
    }

    // Show loading
    loading.style.display = "block";

    result.innerText = "";

    button.disabled = true;
    button.innerText = "Generating...";


    try {

        const response = await fetch("/generate", {

            method: "POST",

            headers: {
                "Content-Type": "application/json"
            },

            body: JSON.stringify({
                task: task,
                text: text
            })

        });


        const data = await response.json();


        if (data.success) {

            result.innerText = data.result;

        } else {

            result.innerText = "Error: " + data.message;

        }


    } catch (error) {

        result.innerText =
            "Something went wrong. Please try again.";

        console.error(error);

    }


    // Hide loading
    loading.style.display = "none";

    button.disabled = false;
    button.innerText = "Generate";
}


function copyResult() {

    const result =
        document.getElementById("result").innerText;

    if (!result.trim()) {

        alert("Nothing to copy.");

        return;
    }

    navigator.clipboard.writeText(result);

    alert("Result copied!");
}