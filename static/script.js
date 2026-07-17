// EduGenie frontend logic
// Handles: capturing user input, calling the backend /generate route,
// showing loading/error states, displaying output, and the copy button.

const courseTitleInput = document.getElementById("courseTitle");
const generateBtn = document.getElementById("generateBtn");
const statusMsg = document.getElementById("statusMsg");
const outputBox = document.getElementById("outputBox");
const outputContent = document.getElementById("outputContent");
const copyBtn = document.getElementById("copyBtn");

async function generateContent() {
  const courseTitle = courseTitleInput.value.trim();

  // --- basic client-side validation ---
  if (!courseTitle) {
    showStatus("Please enter a course title.", true);
    return;
  }

  // --- reset UI state ---
  outputBox.classList.add("hidden");
  generateBtn.disabled = true;
  showStatus("Generating content, please wait...", false);

  try {
    const res = await fetch("/generate", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ course_title: courseTitle }),
    });

    const data = await res.json();

    if (!res.ok) {
      // Server returned an error (bad input, missing key, API failure, etc.)
      showStatus(data.error || "Something went wrong. Please try again.", true);
      return;
    }

    outputContent.textContent = data.content;
    outputBox.classList.remove("hidden");
    showStatus("", false);

  } catch (err) {
    // Network failure or server unreachable
    showStatus("Could not reach the server. Check your connection and try again.", true);
  } finally {
    generateBtn.disabled = false;
  }
}

function showStatus(message, isError) {
  statusMsg.textContent = message;
  statusMsg.classList.toggle("error", isError);
}

copyBtn.addEventListener("click", () => {
  navigator.clipboard.writeText(outputContent.textContent).then(() => {
    const originalText = copyBtn.textContent;
    copyBtn.textContent = "Copied!";
    setTimeout(() => (copyBtn.textContent = originalText), 1500);
  });
});

generateBtn.addEventListener("click", generateContent);

// Allow pressing Enter in the input field to trigger generation
courseTitleInput.addEventListener("keydown", (e) => {
  if (e.key === "Enter") generateContent();
});
