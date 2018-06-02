
/*
    Get error report to errlist
*/
function get_error_msgText( errlist ){
    errlist = eval( errlist );
    var ret = '';
    for(var i = 0 ; i < errlist.length ; ++ i)
        ret = ret + '<li>' + errlist[i] + '</li>';
    return '<ul class=\"list\">' + ret + '</ul>';
}

/*
    content to markdown + katex
*/

function Pewview( content , render ){
    $('#' + content )[0].addEventListener('input' , function(){
       $('#' + render )[0].innerHTML = marked($(this).val());
        renderMathInElement(
        document.getElementById( render ),
        {
            delimiters : [
                {left: "$$", right: "$$", display: true},
                {left: "$", right: "$", display: false},                    
                {left: "\\[", right: "\\]", display: true},
                {left: "\\(", right: "\\)", display: false}
            ]
        });
    });
    $('#' + render )[0].innerHTML = marked( $('#' + content).val() );
}

/*
    return the empty string of string array s
*/
function RemoveEmptyElement( s ){
    let ret = new Array();
    for(let i = 0 ; i < s.length ; ++ i)
        if( s[i].length > 0 )
            ret.push( s[i] );
    return ret;
}

/*
    return the prefix_url of s
*/
function get_prefix_url( s , argumentsnumber ){
    return '/' + RemoveEmptyElement( s.split( '/' ) ).slice( 0 , -argumentsnumber ).join( '/' );
}