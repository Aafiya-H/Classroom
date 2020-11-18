function openCreateClassForm(event){
    var modal = $('#add_class');
    var url = $(event.target).closest('a').attr('href');
    modal.find('.modal-body').html('').load(url,function(){
        modal.modal('show');
        formAjaxSubmit(popup,url)
    });
}