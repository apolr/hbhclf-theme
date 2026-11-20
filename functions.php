<?php
/**
 * HBHCLF theme setup.
 */

if ( ! defined( 'ABSPATH' ) ) {
	exit;
}

add_action( 'after_setup_theme', function () {
	add_theme_support( 'post-thumbnails' );
	add_theme_support( 'responsive-embeds' );
	add_theme_support( 'editor-styles' );
	add_editor_style( 'style.css' );
	add_post_type_support( 'page', 'excerpt' ); // page summary used as the search description
} );

// Motion layer: one small stylesheet and one small script, no libraries.
add_action( 'wp_enqueue_scripts', function () {
	$dir = get_template_directory();
	$uri = get_template_directory_uri();

	// Theme stylesheet: design tokens, header, team cards, galleries.
	wp_enqueue_style(
		'hbhclf-style',
		get_stylesheet_uri(),
		array(),
		(string) filemtime( $dir . '/style.css' )
	);
	wp_enqueue_style(
		'hbhclf-motion',
		$uri . '/assets/css/motion.css',
		array( 'hbhclf-style' ),
		(string) filemtime( $dir . '/assets/css/motion.css' )
	);
	wp_enqueue_script(
		'hbhclf-motion',
		$uri . '/assets/js/motion.js',
		array(),
		(string) filemtime( $dir . '/assets/js/motion.js' ),
		array( 'in_footer' => true, 'strategy' => 'defer' )
	);
} );

// Search and sharing basics (meta description, link previews, structured data, llms.txt).
require_once get_template_directory() . '/inc/seo.php';

/**
 * The MailPoet form prints its own <style> block. The Shortcode block runs
 * wpautop over it, which breaks that CSS with stray <p> tags. Render the
 * MailPoet shortcode cleanly instead.
 */
add_filter( 'render_block', function ( $html, $block ) {
	if ( 'core/shortcode' === ( $block['blockName'] ?? '' ) && false !== strpos( $block['innerHTML'] ?? '', 'mailpoet_form' ) ) {
		return do_shortcode( trim( $block['innerHTML'] ) );
	}
	return $html;
}, 10, 2 );
