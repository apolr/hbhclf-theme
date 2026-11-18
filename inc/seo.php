<?php
/**
 * Search and sharing basics, without an SEO plugin:
 * meta description, Open Graph and Twitter tags, Organization structured data,
 * and an llms.txt summary for AI assistants. WordPress itself already provides
 * the <title> tag and the sitemap at /wp-sitemap.xml.
 */

if ( ! defined( 'ABSPATH' ) ) {
	exit;
}

/** Description for the current view: excerpt, else first words of content, else the site tagline. */
function hbhclf_meta_description() {
	if ( is_singular() ) {
		$post = get_queried_object();
		$text = has_excerpt( $post ) ? get_the_excerpt( $post ) : '';
		if ( ! $text ) {
			// First real paragraph (60+ characters) of the content, so banner lines and labels are skipped.
			$content = (string) $post->post_content;
			if ( preg_match_all( '/<p[^>]*>(.*?)<\/p>/is', $content, $m ) ) {
				foreach ( $m[1] as $para ) {
					$plain = trim( wp_strip_all_tags( strip_shortcodes( $para ) ) );
					if ( mb_strlen( $plain ) >= 60 ) {
						$text = $plain;
						break;
					}
				}
			}
			if ( ! $text ) {
				$text = wp_strip_all_tags( strip_shortcodes( excerpt_remove_blocks( $content ) ) );
			}
		}
	} elseif ( is_category() || is_tag() ) {
		$text = term_description() ? term_description() : single_term_title( '', false ) . ' from ' . get_bloginfo( 'name' );
	} else {
		$text = get_bloginfo( 'description' );
	}
	$text = trim( preg_replace( '/\s+/', ' ', html_entity_decode( wp_strip_all_tags( (string) $text ), ENT_QUOTES ) ) );
	return wp_html_excerpt( $text, 158, '…' );
}

/** Image for link previews: featured image, else first image in the content, else the site logo. */
function hbhclf_share_image() {
	if ( is_singular() ) {
		$id = get_queried_object_id();
		if ( has_post_thumbnail( $id ) ) {
			return get_the_post_thumbnail_url( $id, 'large' );
		}
		if ( preg_match( '/<img[^>]+src="([^"]+)"/i', (string) get_post_field( 'post_content', $id ), $m ) ) {
			return $m[1];
		}
	}
	$logo = get_theme_mod( 'custom_logo' ) ? get_theme_mod( 'custom_logo' ) : get_option( 'site_logo' );
	return $logo ? wp_get_attachment_image_url( (int) $logo, 'full' ) : '';
}

add_action( 'wp_head', function () {
	if ( is_404() ) {
		return;
	}
	$desc  = hbhclf_meta_description();
	$title = wp_get_document_title();
	$url   = is_singular() ? get_permalink() : home_url( add_query_arg( array(), $GLOBALS['wp']->request ) );
	$img   = hbhclf_share_image();
	$type  = is_singular( 'post' ) ? 'article' : 'website';

	echo "\n<!-- HBHCLF search and sharing -->\n";
	if ( $desc ) {
		printf( "<meta name=\"description\" content=\"%s\">\n", esc_attr( $desc ) );
	}
	printf( "<meta property=\"og:site_name\" content=\"%s\">\n", esc_attr( get_bloginfo( 'name' ) ) );
	printf( "<meta property=\"og:type\" content=\"%s\">\n", esc_attr( $type ) );
	printf( "<meta property=\"og:title\" content=\"%s\">\n", esc_attr( $title ) );
	printf( "<meta property=\"og:url\" content=\"%s\">\n", esc_url( $url ) );
	printf( "<meta property=\"og:locale\" content=\"en_CA\">\n" );
	if ( $desc ) {
		printf( "<meta property=\"og:description\" content=\"%s\">\n", esc_attr( $desc ) );
	}
	if ( $img ) {
		printf( "<meta property=\"og:image\" content=\"%s\">\n", esc_url( $img ) );
	}
	printf( "<meta name=\"twitter:card\" content=\"%s\">\n", $img ? 'summary_large_image' : 'summary' );
	if ( is_singular( 'post' ) ) {
		printf( "<meta property=\"article:published_time\" content=\"%s\">\n", esc_attr( get_the_date( 'c' ) ) );
		printf( "<meta property=\"article:modified_time\" content=\"%s\">\n", esc_attr( get_the_modified_date( 'c' ) ) );
	}
	if ( is_search() ) {
		echo "<meta name=\"robots\" content=\"noindex, follow\">\n";
	}

	// Structured data: who the organization is, on every page.
	$logo = get_option( 'site_logo' );
	$org  = array(
		'@type'       => 'NGO',
		'@id'         => home_url( '/#organization' ),
		'name'        => get_bloginfo( 'name' ),
		'alternateName' => 'HBHCLF',
		'url'         => home_url( '/' ),
		'description' => get_bloginfo( 'description' ),
		'email'       => 'info@hbhclf.org',
		'telephone'   => '+1-289-408-8634',
		'foundingDate' => '2021-09-14',
		'address'     => array(
			'@type'           => 'PostalAddress',
			'streetAddress'   => '268-762 Upper James Street',
			'addressLocality' => 'Hamilton',
			'addressRegion'   => 'ON',
			'postalCode'      => 'L9C 3A2',
			'addressCountry'  => 'CA',
		),
		'areaServed'  => 'Hamilton, Ontario',
		'sameAs'      => array( 'https://www.instagram.com/hamiltonblackhealth/' ),
	);
	if ( $logo ) {
		$org['logo'] = wp_get_attachment_image_url( (int) $logo, 'full' );
	}
	$graph = array( $org, array(
		'@type'     => 'WebSite',
		'@id'       => home_url( '/#website' ),
		'url'       => home_url( '/' ),
		'name'      => get_bloginfo( 'name' ),
		'publisher' => array( '@id' => home_url( '/#organization' ) ),
		'inLanguage' => 'en-CA',
	) );
	if ( is_singular( 'post' ) ) {
		$graph[] = array_filter( array(
			'@type'         => 'NewsArticle',
			'headline'      => wp_strip_all_tags( get_the_title() ),
			'datePublished' => get_the_date( 'c' ),
			'dateModified'  => get_the_modified_date( 'c' ),
			'image'         => $img ? array( $img ) : null,
			'url'           => get_permalink(),
			'publisher'     => array( '@id' => home_url( '/#organization' ) ),
			'author'        => array( '@id' => home_url( '/#organization' ) ),
			'description'   => $desc,
		) );
	}
	echo '<script type="application/ld+json">' . wp_json_encode( array( '@context' => 'https://schema.org', '@graph' => $graph ), JSON_UNESCAPED_SLASHES | JSON_UNESCAPED_UNICODE ) . "</script>\n";
}, 2 );

/** /llms.txt: a plain-text guide to the site for AI assistants, built from live pages and posts. */
add_action( 'init', function () {
	$path = isset( $_SERVER['REQUEST_URI'] ) ? strtok( wp_unslash( $_SERVER['REQUEST_URI'] ), '?' ) : '';
	if ( '/llms.txt' !== $path ) {
		return;
	}
	$out   = array();
	$out[] = '# ' . get_bloginfo( 'name' );
	$out[] = '';
	$out[] = '> ' . get_bloginfo( 'description' ) . '. A federally registered, non-partisan, non-profit organization in Hamilton, Ontario, Canada, advocating for the health and well-being of the African Diaspora. Contact: info@hbhclf.org, 289-408-8634.';
	$out[] = '';
	$out[] = '## Pages';
	foreach ( get_pages( array( 'post_status' => 'publish', 'sort_column' => 'menu_order,post_title' ) ) as $p ) {
		$out[] = '- [' . wp_strip_all_tags( $p->post_title ) . '](' . get_permalink( $p ) . ')';
	}
	$out[] = '';
	$out[] = '## News and statements';
	foreach ( get_posts( array( 'numberposts' => 30, 'post_status' => 'publish' ) ) as $p ) {
		$out[] = '- [' . wp_strip_all_tags( $p->post_title ) . '](' . get_permalink( $p ) . '): ' . get_the_date( 'F j, Y', $p );
	}
	$out[] = '';
	$out[] = '## Optional';
	$out[] = '- [Sitemap](' . home_url( '/wp-sitemap.xml' ) . ')';
	nocache_headers();
	header( 'Content-Type: text/plain; charset=utf-8' );
	echo implode( "\n", $out ) . "\n";
	exit;
} );
