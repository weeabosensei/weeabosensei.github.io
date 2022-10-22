/*
	By Osvaldas Valutis, www.osvaldas.info
	Available for use under the MIT License
*/

;( function ( document, window, index )
{
	'use strict';

	var target		= false,
		settings	= {},
		lastKeyUp	= 0,
		keyUpEvent  = false,
		keyUpCode	= false,
		dpTimeout	= false,
		isPaused	= false,

		findElement = function( selector, parent )
		{
			var element = parent || document;
			element = element.querySelectorAll( selector );
			return element.length ? element[ element.length - 1 ] : false;
		},

		findPrevElement = function( element, selector )
		{
			selector = selector || false;
			if( element.previousElementSibling ) element = element.previousElementSibling;
			else do { element = element.previousSibling; } while ( element && element.nodeType !== 1 );
			if( !element ) return false;
			if( selector )
			{
				if( isElement( element, selector ) ) return element;
				else return false;
			}
			return element;
		},

		findNextElement = function( element, selector )
		{
			selector = selector || false;
			if( element.nextElementSibling ) element = element.nextElementSibling;
			else do { element = element.nextSibling; } while ( element && element.nodeType !== 1 );
			if( !element ) return false;
			if( selector )
			{
				if( isElement( element, selector ) ) return element;
				else return false;
			}
			return element;
		},

		isElement = function( element, selector )
		{
			var _matches = ( element.matches || element.matchesSelector || element.msMatchesSelector || element.mozMatchesSelector || element.webkitMatchesSelector || element.oMatchesSelector );
			if( _matches ) return _matches.call( element, selector );
			else
			{
				var nodes = element.parentNode.querySelectorAll( selector );
				for( var i = nodes.length; i--; ) if( nodes[ i ] === element ) return true;
				return false;
			}
		},

		addEventListener = function( element, event, handler )
		{
			if( element.addEventListener )
				element.addEventListener( event, handler );
			else
				element.attachEvent( 'on' + event, function(){ handler.call( element ); });
		},

		navigate = function()
		{
			var item = false;

			if( keyUpCode == settings.keyCodeLeft && settings.prev )
				item = findElement( settings.prev, target );

			else if( keyUpCode == settings.keyCodeRight && settings.next )
				item = findElement( settings.next, target );

			if( !item && settings.num && settings.numCurrent )
			{
				item = findElement( settings.numCurrent, target );
				if( item ) item = keyUpCode == settings.keyCodeLeft ? findPrevElement( item, settings.num ) : findNextElement( item, settings.num );
			}

			if( item )
			{
				item = findElement( 'a', item );
				if( item ) item.click();
			}
		};

	addEventListener( document, 'keyup', function( e )
	{
		keyUpEvent	= e || window.event;
		keyUpCode	= keyUpEvent.keyCode;

		if( !target || isPaused || ( keyUpCode != settings.keyCodeLeft && keyUpCode != settings.keyCodeRight ) )
			return true;

		keyUpEvent.preventDefault ? keyUpEvent.preventDefault() : keyUpEvent.returnValue = false;

		if( settings.first || settings.last )
		{
			if( new Date() - lastKeyUp <= settings.doublePressInt )
			{
				clearTimeout( dpTimeout );

				var item = false;

				if( keyUpCode == settings.keyCodeLeft && settings.first )
					item = findElement( settings.first, target );

				else if( keyUpCode == settings.keyCodeRight && settings.last )
					item = findElement( settings.last, target );

				if( item )
				{
					item = findElement( 'a', item );
					if( item ) item.click();
				}
				if( !item ) navigate();
			}
			else dpTimeout = setTimeout( navigate, settings.doublePressInt );

			lastKeyUp = new Date();
		}
		else navigate();
	});

	var keyboardPagination = function( selector, options )
	{
		var KeyboardPagination = function( selector, options )
		{
			settings =	{
							num:			false,
							numCurrent:		false,
							prev:			false,
							next:			false,
							first:			false,
							last:			false,
							doublePressInt: 250,
							keyCodeLeft:	37,
							keyCodeRight:	39
						};
			var i;
			for( i in options )
				settings[ i ] = options[ i ];

			target = findElement( selector );

			isPaused = false;
		};

		KeyboardPagination.prototype =
		{
			resume: function()
			{
				isPaused = false;
			},
			pause: function()
			{
				isPaused = true;
			},
		};

		return new KeyboardPagination( selector, options );
	};

	window.keyboardPagination = keyboardPagination;

}( document, window, 0 ));