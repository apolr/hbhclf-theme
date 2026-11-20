/*
 * HBHCLF motion layer script. No dependencies.
 * Cycles hero slides, and reveals blocks as they scroll into view.
 */
( function () {
	'use strict';

	var root = document.documentElement;
	root.classList.add( 'hb-js' );

	var reduce = window.matchMedia && window.matchMedia( '(prefers-reduced-motion: reduce)' ).matches;
	var INTERVAL = 7000;

	function initHero( hero ) {
		var slides = Array.prototype.slice.call( hero.querySelectorAll( ':scope > .hb-hero__slide' ) );
		if ( slides.length === 0 ) {
			return;
		}
		var current = 0;
		var timer = null;

		slides[ 0 ].classList.add( 'is-active' );
		if ( slides.length === 1 ) {
			return;
		}

		var dots = document.createElement( 'div' );
		dots.className = 'hb-hero__dots';
		var buttons = slides.map( function ( slide, i ) {
			var b = document.createElement( 'button' );
			b.type = 'button';
			b.setAttribute( 'aria-label', 'Show slide ' + ( i + 1 ) + ' of ' + slides.length );
			b.addEventListener( 'click', function () {
				show( i );
				restart();
			} );
			dots.appendChild( b );
			return b;
		} );
		hero.appendChild( dots );

		function show( index ) {
			slides[ current ].classList.remove( 'is-active' );
			current = ( index + slides.length ) % slides.length;
			slides[ current ].classList.add( 'is-active' );
			buttons.forEach( function ( b, i ) {
				if ( i === current ) {
					b.setAttribute( 'aria-current', 'true' );
				} else {
					b.removeAttribute( 'aria-current' );
				}
			} );
		}

		function start() {
			if ( reduce || timer ) {
				return;
			}
			timer = window.setInterval( function () {
				show( current + 1 );
			}, INTERVAL );
		}
		function stop() {
			window.clearInterval( timer );
			timer = null;
		}
		function restart() {
			stop();
			start();
		}

		show( 0 );
		start();

		hero.addEventListener( 'mouseenter', stop );
		hero.addEventListener( 'mouseleave', start );
		hero.addEventListener( 'focusin', stop );
		hero.addEventListener( 'focusout', start );
		document.addEventListener( 'visibilitychange', function () {
			if ( document.hidden ) {
				stop();
			} else {
				start();
			}
		} );
	}

	function initReveal() {
		var items = document.querySelectorAll( '.hb-reveal' );
		if ( ! items.length ) {
			return;
		}
		if ( reduce || ! ( 'IntersectionObserver' in window ) ) {
			items.forEach( function ( el ) {
				el.classList.add( 'is-visible' );
			} );
			return;
		}
		var io = new IntersectionObserver(
			function ( entries ) {
				entries.forEach( function ( entry ) {
					if ( entry.isIntersecting ) {
						entry.target.classList.add( 'is-visible' );
						io.unobserve( entry.target );
					}
				} );
			},
			{ threshold: 0.15, rootMargin: '0px 0px -5% 0px' }
		);
		items.forEach( function ( el ) {
			io.observe( el );
		} );
	}

	// Decorative floating shapes in the hero and on full-width coloured bands.
	function addShapes( el ) {
		if ( el.querySelector( ':scope > .hb-shapes' ) ) {
			return;
		}
		var wrap = document.createElement( 'div' );
		wrap.className = 'hb-shapes';
		wrap.setAttribute( 'aria-hidden', 'true' );
		for ( var i = 1; i <= 5; i++ ) {
			var s = document.createElement( 'span' );
			s.className = 'hb-shape hb-shape--' + i;
			wrap.appendChild( s );
		}
		el.classList.add( 'hb-has-shapes' );
		el.insertBefore( wrap, el.firstChild );
	}

	// Logo rows become a slow sideways scroller (content duplicated once for a seamless loop).
	function initMarquee( row ) {
		if ( row.closest( '.hb-marquee' ) || row.children.length < 4 ) {
			return;
		}
		var outer = document.createElement( 'div' );
		outer.className = 'hb-marquee';
		row.parentNode.insertBefore( outer, row );
		outer.appendChild( row );
		row.classList.add( 'hb-marquee__track' );
		Array.prototype.slice.call( row.children ).forEach( function ( child ) {
			var copy = child.cloneNode( true );
			copy.setAttribute( 'aria-hidden', 'true' );
			copy.querySelectorAll( 'img' ).forEach( function ( img ) { img.alt = ''; } );
			row.appendChild( copy );
		} );
		row.style.setProperty( '--hb-marquee', ( row.children.length * 3 ) + 's' );
	}

	/* Mobile menu: add the logo at the top and Donate plus Instagram at the bottom of the overlay. */
	function initMobileMenu() {
		document.querySelectorAll( '.hb-nav .wp-block-navigation__responsive-container-content' ).forEach( function ( box ) {
			if ( box.querySelector( '.hb-menu-extra' ) ) { return; }
			var header = box.closest( 'header' ) || document;
			var logo = header.querySelector( '.hb-logo img' );
			if ( logo ) {
				var top = document.createElement( 'div' );
				top.className = 'hb-menu-extra hb-menu-logo';
				var a = document.createElement( 'a' );
				a.href = '/';
				a.setAttribute( 'aria-label', 'Home' );
				var img = logo.cloneNode( false );
				img.removeAttribute( 'srcset' );
				img.removeAttribute( 'width' );
				img.removeAttribute( 'height' );
				a.appendChild( img );
				top.appendChild( a );
				box.insertBefore( top, box.firstChild );
			}
			var foot = document.createElement( 'div' );
			foot.className = 'hb-menu-extra hb-menu-foot';
			var donate = header.querySelector( '.hb-donate a' );
			if ( donate ) {
				var d = donate.cloneNode( true );
				d.className = 'hb-menu-donate';
				foot.appendChild( d );
			}
			var insta = header.querySelector( '.hb-social a' );
			if ( insta ) {
				var i = insta.cloneNode( true );
				i.className = 'hb-menu-social';
				i.insertAdjacentHTML( 'beforeend', '<span>Follow us on Instagram</span>' );
				foot.appendChild( i );
			}
			box.appendChild( foot );
		} );
	}

	function init() {
		initMobileMenu();
		document.querySelectorAll( '.hb-hero' ).forEach( function ( hero ) {
			initHero( hero );
			addShapes( hero );
		} );
		document.querySelectorAll( '.wp-block-post-content > .alignfull.has-background:not(.hb-hero)' ).forEach( function ( band ) {
			band.classList.add( 'hb-band' );
			addShapes( band );
		} );
		document.querySelectorAll( '.hb-logos' ).forEach( initMarquee );
		initReveal();
	}

	if ( document.readyState === 'loading' ) {
		document.addEventListener( 'DOMContentLoaded', init );
	} else {
		init();
	}
} )();
