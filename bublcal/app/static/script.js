// Creates a bubble
function createBubble(button)
{
    var text    = prompt("New Bubble", "<text>");
    var holder  = button.parentNode;
    var bubble  = document.createElement("button");

    bubble.setAttribute("onclick", "killme(this);");
    bubble.classList.add("bub");

    bubble.textContent = text;
    holder.appendChild(bubble);
}

// Kills a bubble when clicked on 
function killme(passed)
{
    passed.classList.add("bubPopAnimate");

    function whichTransitionEvent()
    {
        var t;
        var el = document.createElement('fakeelement');
        var transitions = 
        {
            'transition':'transitionend',
            'OTransition':'oTransitionEnd',
            'MozTransition':'transitionend',
            'WebkitTransition':'webkitTransitionEnd'
        }

        for(t in transitions)
        {
            if(el.style[t] !== undefined)
            {
                return transitions[t];
            }
        }
    }

    var transitionEvent = whichTransitionEvent();
    transitionEvent && passed.addEventListener(transitionEvent, function()
    {
        if(passed != null)
        {
            this.parentElement.removeChild(passed);
        }
    });
}