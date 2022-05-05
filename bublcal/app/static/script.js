function display_ct7()
{
    var x = new Date();
    var ampm = x.getHours( ) >= 12 ? ' PM' : ' AM';
    
    hours = x.getHours( ) % 12;
    hours = hours ? hours : 12;
    hours = hours.toString().length == 1 ? 0 + hours.toString() : hours;

    var minutes = x.getMinutes().toString();
    minutes = minutes.length==1 ? 0+minutes : minutes;

    var seconds = x.getSeconds().toString();
    seconds = seconds.length == 1 ? 0 + seconds : seconds;

    var month = (x.getMonth() + 1).toString();
    month = month.length == 1 ? 0 + month : month;

    var dt = x.getDate().toString();
    dt = dt.length == 1 ? 0 + dt : dt;

    var x1 = month + "/" + dt + "/" + x.getFullYear();
    x1 = x1 + " - " +  hours + ":" +  minutes + ":" +  seconds + " " + ampm;
    
    document.getElementById('ct7').innerHTML = x1;
    display_c7();
}

function display_c7()
{
    var refresh = 1000; // Refresh rate in milli seconds
    let url = window.location.href.split("/");

    for(var i = 0; i < url.length; i++)
    {
        if(url[i] == "glance")
        {
            // Get the required tags
            dateElement   = document.getElementsByName("date");
            timeElement   = document.getElementsByName("time");
            
            if(dateElement.length > 0 && timeElement.length > 0)
            {
                // Only set it once
                if(dateElement[0].value == "" && dateElement[0].value == "")
                {
                    // Get todays year, month, and day
                    today   = new Date();
                    year    = today.getFullYear();
                    month   = today.getMonth() + 1;
                    day     = today.getDate();
                    hour    = today.getHours();
                    minute  = today.getMinutes();

                    // Zero padding
                    month   = ((month < 10) ? "0" : "") + month.toString();
                    day     = ((day < 10) ? "0" : "") + day.toString();
                    hour    = ((hour < 10) ? "0" : "") + hour.toString();
                    minute  = ((minute < 10) ? "0" : "") + minute.toString();

                    dateElement[0].value = `${year}-${month}-${day}`;
                    timeElement[0].value = `${hour}:${minute}`;
                }
            }
        }
        
        if(url[i] == "daily")
        {
            // Get the required tags
            dateElement   = document.getElementsByName("date");
            
            if(dateElement.length > 0)
            {
                // Only set it once
                if(dateElement[0].value == "")
                {
                    // Get todays year, month, and day
                    today   = new Date();
                    year    = url[7];
                    month   = url[5];
                    day     = url[6];

                    // Zero padding 
                    if(month.length < 2)    { month = ((month < 10) ? "0" : "") + month.toString(); }
                    if(day.length < 2)      { day   = ((day < 10)   ? "0" : "") + day.toString();   }

                    dateElement[0].value = `${year}-${month}-${day}`;
                }
            }
        }
    }

    mytime = setTimeout("display_ct7()", refresh);
}

display_c7();