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
} );

// Motion layer: one small stylesheet and one small script, no libraries.
add_action( 'wp_enqueue_scripts', function () {
	$dir = get_template_directory();
	$uri = get_template_directory_uri();

	wp_enqueue_style(
		'hbhclf-motion',
		$uri . '/assets/css/motion.css',
		array(),
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
