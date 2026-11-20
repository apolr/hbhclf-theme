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
	foreach ( hbhclf_extra_schema( $url ) as $node ) {
		$graph[] = $node;
	}
	echo '<script type="application/ld+json">' . wp_json_encode( array( '@context' => 'https://schema.org', '@graph' => $graph ), JSON_UNESCAPED_SLASHES | JSON_UNESCAPED_UNICODE ) . "</script>\n";
}, 2 );

/** Question-and-answer pairs found in "Details" blocks on a page (FAQ sections). */
function hbhclf_collect_faq( $blocks, &$out ) {
	foreach ( $blocks as $b ) {
		if ( 'core/details' === $b['blockName'] ) {
			$q = trim( wp_strip_all_tags( isset( $b['attrs']['summary'] ) ? $b['attrs']['summary'] : '' ) );
			if ( ! $q && preg_match( '/<summary>(.*?)<\/summary>/is', $b['innerHTML'], $m ) ) {
				$q = trim( wp_strip_all_tags( $m[1] ) );
			}
			$a = '';
			foreach ( $b['innerBlocks'] as $inner ) {
				$a .= ' ' . trim( wp_strip_all_tags( render_block( $inner ) ) );
			}
			$a = trim( preg_replace( '/\s+/', ' ', $a ) );
			if ( $q && $a ) {
				$out[] = array(
					'@type'          => 'Question',
					'name'           => html_entity_decode( $q, ENT_QUOTES ),
					'acceptedAnswer' => array( '@type' => 'Answer', 'text' => html_entity_decode( $a, ENT_QUOTES ) ),
				);
			}
		} elseif ( ! empty( $b['innerBlocks'] ) ) {
			hbhclf_collect_faq( $b['innerBlocks'], $out );
		}
	}
}

/** Breadcrumbs, FAQ and event data for the current page. */
function hbhclf_extra_schema( $url ) {
	$nodes = array();

	// Breadcrumbs (Home > parent > page, or Home > News > post).
	if ( is_singular() && ! is_front_page() ) {
		$post  = get_queried_object();
		$trail = array( array( 'Home', home_url( '/' ) ) );
		if ( is_singular( 'post' ) ) {
			$cats = get_the_category( $post->ID );
			if ( $cats ) {
				$trail[] = array( $cats[0]->name, get_category_link( $cats[0] ) );
			}
		} else {
			$parents = array_reverse( get_post_ancestors( $post ) );
			foreach ( $parents as $pid ) {
				$trail[] = array( wp_strip_all_tags( get_the_title( $pid ) ), get_permalink( $pid ) );
			}
		}
		$trail[] = array( wp_strip_all_tags( get_the_title( $post ) ), $url );
		$items   = array();
		foreach ( $trail as $i => $t ) {
			$items[] = array( '@type' => 'ListItem', 'position' => $i + 1, 'name' => html_entity_decode( $t[0], ENT_QUOTES ), 'item' => $t[1] );
		}
		$nodes[] = array( '@type' => 'BreadcrumbList', 'itemListElement' => $items );
	}

	// FAQ: every "Details" block on the page becomes a question and answer.
	if ( is_singular( 'page' ) ) {
		$faq = array();
		hbhclf_collect_faq( parse_blocks( (string) get_post_field( 'post_content', get_queried_object_id() ) ), $faq );
		if ( $faq ) {
			$nodes[] = array( '@type' => 'FAQPage', 'mainEntity' => $faq );
		}
	}

	// The Baobab Tree community launch, on the pages that talk about it, until it has happened.
	$launch_end = strtotime( '2026-12-15 19:30:00 America/Toronto' );
	if ( time() < $launch_end && ( is_front_page() || is_page( 'inahita-kijiji-kulea-mtoto' ) || ( is_singular( 'page' ) && 1780 === get_queried_object_id() ) ) ) {
		$nodes[] = array(
			'@type'               => 'Event',
			'name'                => 'Come Let Us Meet Under the Baobab Tree: Inahitaji Kijiji Kulea Mtoto community launch',
			'description'         => 'A community launch for Inahitaji Kijiji Kulea Mtoto (It Takes a Village to Raise a Child), HBHCLF’s wrap-around support initiative for Black/African and newcomer families in Hamilton.',
			'startDate'           => '2026-12-15T18:00:00-05:00',
			'endDate'             => '2026-12-15T19:30:00-05:00',
			'eventStatus'         => 'https://schema.org/EventScheduled',
			'eventAttendanceMode' => 'https://schema.org/OfflineEventAttendanceMode',
			'location'            => array(
				'@type'   => 'Place',
				'name'    => 'Hamilton Urban Core Community Health Centre',
				'address' => array(
					'@type'           => 'PostalAddress',
					'streetAddress'   => '430 Cannon Street East',
					'addressLocality' => 'Hamilton',
					'addressRegion'   => 'ON',
					'postalCode'      => 'L8L 2C8',
					'addressCountry'  => 'CA',
				),
			),
			'organizer'           => array( '@id' => home_url( '/#organization' ) ),
			'isAccessibleForFree' => true,
		);
	}
	return $nodes;
}

/** Keep search engines focused on real content: no author pages, no MailPoet system pages in search. */
add_action( 'template_redirect', function () {
	if ( is_author() ) {
		wp_safe_redirect( home_url( '/' ), 301 );
		exit;
	}
} );
add_filter( 'wp_sitemaps_add_provider', function ( $provider, $name ) {
	return 'users' === $name ? false : $provider;
}, 10, 2 );
add_filter( 'wp_sitemaps_post_types', function ( $types ) {
	unset( $types['mailpoet_page'] );
	return $types;
} );
add_filter( 'wp_robots', function ( $robots ) {
	if ( is_singular( 'mailpoet_page' ) || is_attachment() ) {
		$robots['noindex'] = true;
		$robots['follow']  = true;
		unset( $robots['max-image-preview'] );
	}
	return $robots;
} );
// Do not list login names to visitors who are not signed in.
add_filter( 'rest_endpoints', function ( $endpoints ) {
	if ( ! is_user_logged_in() ) {
		unset( $endpoints['/wp/v2/users'], $endpoints['/wp/v2/users/(?P<id>[\d]+)'] );
	}
	return $endpoints;
} );

/** Faster galleries: lazy loading, and a right-sized image for each screen, on news posts. */
add_filter( 'the_content', function ( $html ) {
	if ( ! is_singular( 'post' ) || ! in_the_loop() ) {
		return $html;
	}
	return preg_replace_callback( '/<img\b[^>]*>/i', function ( $m ) {
		$tag = $m[0];
		if ( false === stripos( $tag, 'loading=' ) ) {
			$tag = preg_replace( '/<img\b/i', '<img loading="lazy" decoding="async"', $tag, 1 );
		}
		if ( false === stripos( $tag, 'srcset=' ) && preg_match( '/\bsrc="([^"]+)"/i', $tag, $s ) ) {
			$key = 'hb_srcset_' . md5( $s[1] );
			$set = wp_cache_get( $key, 'hbhclf' );
			if ( false === $set ) {
				$id  = attachment_url_to_postid( $s[1] );
				$set = $id ? (string) wp_get_attachment_image_srcset( $id, 'full' ) : '';
				wp_cache_set( $key, $set, 'hbhclf', HOUR_IN_SECONDS );
			}
			if ( $set ) {
				$tag = preg_replace( '/<img\b/i', '<img srcset="' . esc_attr( $set ) . '" sizes="(max-width: 900px) 100vw, 900px"', $tag, 1 );
			}
		}
		return $tag;
	}, $html );
}, 30 );

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
	$out[] = '## About';
	$out[] = '- Established September 14, 2021 and inaugurated May 28, 2022. Serves people of African heritage in Hamilton and speaks for the community to the City of Hamilton and the provincial and federal governments, with a focus on the social determinants of health.';
	$out[] = '- Address: 268-762 Upper James Street, Hamilton, ON L9C 3A2';
	$out[] = '';
	$out[] = '## Programs';
	$out[] = '- Inahitaji Kijiji Kulea Mtoto (It Takes a Village to Raise a Child): wrap-around support for racialized Black/African and newcomer families in Hamilton engaged with the child-welfare system. ' . home_url( '/inahita-kijiji-kulea-mtoto/' );
	$out[] = '- ABUSUA Elder volunteer program: ' . home_url( '/inahita-kijiji-kulea-mtoto/abusua-elder-volunteer/' );
	$out[] = '- Vaccine Ambassador Program, MentorAction with Interval House of Hamilton, an African Outreach Worker for violence against women support, and a seniors program with NURU Hamilton: ' . home_url( '/programs/' );
	$out[] = '- Newcomer Questionnaire: ' . home_url( '/newcomer_questionnaire/' );
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
