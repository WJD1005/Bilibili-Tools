setInterval(()=>{
    let likebtn=document.querySelector("div.bili-dyn-item__footer > div:nth-child(3) > div[class='bili-dyn-action like']")
    if(likebtn){
        likebtn.click();
    }else{
        let newdynbtn=document.querySelector("div.bili-dyn-list > div.bili-dyn-list__notification.fs-small")
        if(newdynbtn){
            newdynbtn.click();
        }
    }
 }, 1000)