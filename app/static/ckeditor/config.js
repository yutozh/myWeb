/**
 * @license Copyright (c) 2003-2015, CKSource - Frederico Knabben. All rights reserved.
 * For licensing, see LICENSE.md or http://ckeditor.com/license
 */

CKEDITOR.editorConfig = function( config ) {
	config.toolbarGroups = [
		{ name: 'document', groups: [ 'mode', 'document', 'doctools' ] },
		{ name: 'clipboard', groups: [ 'clipboard', 'undo' ] },
		{ name: 'editing', groups: [ 'find', 'selection', 'spellchecker', 'editing' ] },
		{ name: 'forms', groups: [ 'forms' ] },
		'/',
		{ name: 'basicstyles', groups: [ 'basicstyles', 'cleanup' ] },
		{ name: 'paragraph', groups: [ 'list', 'indent', 'blocks', 'align', 'bidi', 'paragraph' ] },
		{ name: 'links', groups: [ 'links' ] },
		{ name: 'insert', groups: [ 'insert' ] },
		'/',
		{ name: 'styles', groups: [ 'styles' ] },
		{ name: 'colors', groups: [ 'colors' ] },
		{ name: 'tools', groups: [ 'tools' ] },
		{ name: 'others', groups: [ 'others' ] },
		{ name: 'about', groups: [ 'about' ] }
	];

	config.removeButtons = 'Form,TextField,Textarea,Select,Radio,Checkbox,ImageButton,Button,HiddenField,About,Scayt,Source';
	config.language = 'zh-cn';
	config.uiColor = '#2FB0FF';
    config.height = "600";
    config.width = "90%";

    config.font_names='宋体/宋体;黑体/黑体;仿宋/仿宋_GB2312;楷体/楷体_GB2312;隶书/隶书;幼圆/幼圆;微软雅黑/微软雅黑;'+ config.font_names;
    config.defaultLanguage = 'zh-cn';
    config.font_defaultLabel = '宋体';
    config.fontSize_defaultLabel = '18';

    config.filebrowserImageBrowseUrl = '../editor/ckfinder/ckfinder.html?Type=Images';
	config.filebrowserFlashBrowseUrl = '../editor/ckfinder/ckfinder.html?Type=Flash';
	config.filebrowserUploadUrl = '/ckupload/';
	config.filebrowserImageUploadUrl = '/ckupload/';
	config.filebrowserFlashUploadUrl = '/ckupload/';
	config.filebrowserWindowWidth = '800';  //“浏览服务器”弹出框的size设置
	config.filebrowserWindowHeight = '500';
	
};