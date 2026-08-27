const tagSelect = document.getElementById("id_tags");
const selectedTags = document.getElementById("selected-tags");

tagSelect.addEventListener("change", function() {

    selectedTags.innerHTML = "";

    for (const option of tagSelect.selectedOptions) {

        const chip = document.createElement("span");

        chip.classList.add("tag-chip");
        chip.textContent = option.text;

        selectedTags.appendChild(chip);
    }

});