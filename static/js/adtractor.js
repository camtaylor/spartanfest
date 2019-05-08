function getWeb3(callback) {
  if (typeof window.web3 === 'undefined') {
    // no web3, use fallback
    console.error("Please use a web3 browser");
  } else {
    // window.web3 == web3 most of the time. Don't override the provided,
    // web3, just wrap it in your Web3.
    var myWeb3 = new Web3(window.web3.currentProvider);

    // the default account doesn't seem to be persisted, copy it to our
    // new instance
    myWeb3.eth.defaultAccount = window.web3.eth.defaultAccount;
    var account = web3.eth.defaultAccount;
    callback(myWeb3);
  }
}

window.addEventListener('load', function() {
  getWeb3(startApp);
});

function startApp(myWeb3) {
    var account = myWeb3.eth.defaultAccount;
    console.log(account);
    $.ajax({
			url: '/refer',
			data: JSON.stringify({'account' : account}),
            contentType: 'application/json;charset=UTF-8',
			type: 'POST',
			success: function(response){
				console.log(response);
			},
			error: function(error){
				console.log(error);
			}
		});
}