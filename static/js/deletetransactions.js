function deleteTransaction(currentId){
  if(document.oldData === undefined)
    document.oldData = {};
  document.oldData ["row_"+currentId] = $('.trash_'+currentId).closest('tr').html();
  $('.trash_'+currentId).closest('td').html('<a href="/transactions/'+currentId+'/delete"><button formaction="/transactions/'+currentId+'/delete" data-transaction-id="'+currentId+'" class="pure-button button-primary">Confirm</button></a><button data-transaction-id="'+currentId+'" onclick="negateDeletion('+currentId+')" class="pure-button button-primary">Cancel</button>');
};

function negateDeletion(currentId){
  $('#delete_'+currentId).closest('tr').html(document.oldData["row_"+currentId]);
}
